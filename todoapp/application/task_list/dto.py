from typing import TypeAlias
from uuid import UUID

from todoapp.application.common.dto import DTO
from todoapp.application.common.pagination import PaginatedItemsDTO
from todoapp.domain.tasks_list.entities import TaskListDetails

TaskListsDTO: TypeAlias = PaginatedItemsDTO[TaskListDetails]


class FindTaskListsFilters(DTO):
    user_id: UUID
    name: str | None = None
