from typing import NewType, Annotated
from uuid import UUID

from pydantic import Field

from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId

TaskId = NewType("TaskId", UUID)


class Task(BaseEntity[TaskId]):
    user_id: UserId
    name: Annotated[str, Field(min_length=3, max_length=500)]
    desc: Annotated[str | None, Field(default=None, max_length=2000)]
    completed_at: DateTimeNull = None
    list_id: ListId | None = None
