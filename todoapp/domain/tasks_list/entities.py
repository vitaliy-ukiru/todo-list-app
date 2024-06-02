from typing import Annotated

from pydantic import Field

from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


class TaskList(BaseEntity[ListId]):
    name: Annotated[str, Field(min_length=3, max_length=500)]
    user_id: UserId
    deleted_at: DateTimeNull = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_have_access(self, user_id: UserId) -> bool:
        return self.user_id == user_id
