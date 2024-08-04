from datetime import datetime
from typing import Annotated, Self

from pydantic import Field
from uuid6 import uuid7

from todoapp.domain.access import Operation
from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.task.constants import MIN_NAME_LENGTH, MAX_NAME_LENGTH, MAX_DESC_LENGTH
from todoapp.domain.task.exceptions import (TaskNameOutOfRange, TaskDescOutOfRange,
                                            MoveTaskToRestrictedList)
from todoapp.domain.task.value_objects import TaskId
from todoapp.domain.task_list.entities import TaskList
from todoapp.domain.user.entities import UserId


class Task(BaseEntity[TaskId]):
    user_id: UserId
    name: Annotated[str, Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)]
    desc: Annotated[str | None, Field(default=None, max_length=MAX_DESC_LENGTH)]
    completed_at: DateTimeNull = None
    list: TaskList | None = None

    @classmethod
    def create(
        cls,
        name: str,
        user_id: UserId,
        desc: str | None = None,
        task_list: TaskList | None = None,
    ) -> Self:

        created_at = datetime.utcnow()
        task_id = TaskId(uuid7())

        return cls(
            id=task_id,
            user_id=user_id,
            name=name,
            desc=desc,
            list=task_list,
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

    def is_have_access(self, user_id: UserId, op: Operation) -> bool:
        is_task_creator = self.user_id == user_id

        if not self.list:
            return is_task_creator  # If task don't have list, access have only owner

        if user_id == self.list.user_id:  # Owner of list also have full access
            return True

        if op is Operation.update_task and is_task_creator:
            # Task's creator, can update task if he's collaborators
            # But he can don't have access to update tasks in list
            return user_id in self.list.sharing.collaborators

        return self.list.is_have_access(user_id, op)

    @property
    def completed(self) -> bool:
        return self.completed_at is not None

    def complete(self):
        if self.completed:
            self.completed_at = None
        else:
            self.completed_at = datetime.utcnow()

    def set_list(self, task_list: TaskList):
        # If collaborator tries to put task in list, that closed for task's author
        # this action must be restricted.
        if not task_list.is_have_access(self.user_id, Operation.read):
            raise MoveTaskToRestrictedList()

        self.list = task_list
