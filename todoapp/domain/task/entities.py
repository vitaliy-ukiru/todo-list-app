from datetime import datetime
from typing import NewType, Annotated, Self
from uuid import UUID

from pydantic import Field
from uuid6 import uuid7

from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.task.constants import MIN_NAME_LENGTH, MAX_NAME_LENGTH, MAX_DESC_LENGTH
from todoapp.domain.task.exceptions import TaskNameOutOfRange, TaskDescOutOfRange
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId

TaskId = NewType("TaskId", UUID)


class Task(BaseEntity[TaskId]):
    user_id: UserId
    name: Annotated[str, Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)]
    desc: Annotated[str | None, Field(default=None, max_length=MAX_DESC_LENGTH)]
    completed_at: DateTimeNull = None
    list_id: ListId | None = None

    @classmethod
    def create(
        cls,
        name: str,
        user_id: UserId,
        desc: str | None = None,
        list_id: ListId | None = None,
    ) -> Self:
        created_at = datetime.utcnow()
        task_id = TaskId(uuid7())

        return cls(
            id=task_id,
            user_id=user_id,
            name=name,
            desc=desc,
            list_id=list_id,
            created_at=created_at,
        )

    def set_name(self, name: str):
        if MIN_NAME_LENGTH <= len(name) <= MAX_NAME_LENGTH:
            raise TaskNameOutOfRange()

        self.name = name

    def set_desc(self, desc: str | None):
        if desc is None:
            self.desc = None
            return

        if desc > MAX_DESC_LENGTH:
            raise TaskDescOutOfRange()

        self.desc = desc

    def is_have_access(self, user_id: UserId) -> bool:
        return user_id == self.user_id

    @property
    def completed(self) -> bool:
        return self.completed_at is not None

    def complete(self):
        if self.completed:
            self.completed_at = None
        else:
            self.completed_at = datetime.utcnow()
