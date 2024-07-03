from typing import TypeAlias
from uuid import UUID

from todoapp.application.common.dto import DTO
from todoapp.application.common.pagination import PaginatedItemsDTO
from todoapp.domain.common.constants import Empty
from todoapp.domain.task.entities import Task
from todoapp.domain.user.entities import UserId

TasksDTO: TypeAlias = PaginatedItemsDTO[Task]


class FindTasksFilters(DTO):
    user_id: UserId
    name: str | None = None
    desc: str | None = None
    completed: bool | Empty = Empty.UNSET
    list_id: UUID | None | Empty = Empty.UNSET
