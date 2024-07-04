from datetime import datetime
from typing import TypeAlias, Self
from uuid import UUID

from todoapp.application.common.dto import DTO
from todoapp.application.common.pagination import PaginatedItemsDTO
from todoapp.domain.common.constants import Empty
from todoapp.domain.common.value_objects import DateTimeNull
from todoapp.domain.task import entities
from todoapp.domain.user.entities import UserId


class FindTasksFilters(DTO):
    user_id: UserId
    name: str | None = None
    desc: str | None = None
    completed: bool | Empty = Empty.UNSET
    list_id: UUID | None | Empty = Empty.UNSET
    shared_access: bool | Empty = Empty.UNSET


class Task(DTO):
    id: UUID
    user_id: UUID
    name: str
    desc: str | None
    completed_at: DateTimeNull = None
    list_id: UUID | None = None
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: entities.Task) -> Self:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            desc=entity.desc,
            completed_at=entity.completed_at,
            list_id=entity.list.id if entity.list else None,
            created_at=entity.created_at,
        )


TasksDTO: TypeAlias = PaginatedItemsDTO[Task]