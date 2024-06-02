from typing import Annotated

from pydantic import Field

from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import User


class TaskList(BaseEntity[ListId]):
    name: Annotated[str, Field(min_length=3, max_length=500)]
    user: User
    deleted_at: DateTimeNull = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
