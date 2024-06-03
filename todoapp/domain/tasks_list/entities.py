from datetime import datetime
from typing import Annotated, Self

from pydantic import Field, model_validator
from uuid6 import uuid7

from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.task.entities import Task
from todoapp.domain.tasks_list.exception import TaskInListConflict, TaskAlreadyInList
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


class TaskListDetails(BaseEntity[ListId]):
    name: Annotated[str, Field(min_length=3, max_length=500)]
    user_id: UserId

    def is_have_access(self, user_id: UserId) -> bool:
        return self.user_id == user_id

    @classmethod
    def create(
        cls,
        name: str,
        user_id: UserId,
    ) -> Self:
        created_at = datetime.utcnow()
        list_id = ListId(uuid7())
        return cls(
            id=list_id,
            name=name,
            user_id=user_id,
            created_at=created_at,
        )


class TaskList(TaskListDetails):
    tasks: Annotated[list[Task], Field(default_factory=list)]

    @model_validator(mode="after")
    def validate_tasks_list_field(self) -> Self:
        for task in self.tasks:
            if task.list_id != self.id:
                raise TaskInListConflict(task.id, self.id)

        return self

    def add_task(self, task: Task):
        if not task.is_have_access(self.user_id):
            raise TaskAccessError(task.id)

        if task.list_id == self.id:
            raise TaskAlreadyInList(task.id, self.id)

        if task in self.tasks:
            raise TaskAlreadyInList(task.id, self.id) \
                from TaskInListConflict(task.id, self.id)

        task.list_id = task
        self.tasks.append(task)

    def move_tasks_another_list(self, task_list: Self):
        if not task_list.is_have_access(self.user_id):
            raise TaskListAccessError(task_list.id)

        for task in self.tasks:
            task.list_id = task_list.id

        task_list.tasks.extend(self.tasks)
        self.tasks.clear()
