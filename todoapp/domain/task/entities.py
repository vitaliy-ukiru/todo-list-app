from typing import NewType, Annotated

from pydantic import UUID4, Field

from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entitites import User

TaskId = NewType("TaskId", UUID4)


class TaskItem(BaseEntity[TaskId]):
    name: Annotated[str, Field(min_length=3, max_length=500)]
    desc: Annotated[str, Field(max_length=2000)]
    completed_at: DateTimeNull = None


class Task(TaskItem):
    user: User
    list_id: ListId | None = None
