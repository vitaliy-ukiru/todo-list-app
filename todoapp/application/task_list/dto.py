from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from todoapp.application.common.dto import DTO
from todoapp.application.common.pagination import PaginatedItemsDTO
from todoapp.domain.task.entities import Task


class TaskListDetails(DTO):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime


TaskListsDTO: TypeAlias = PaginatedItemsDTO[TaskListDetails]


class TaskList(TaskListDetails):
    tasks: list[Task]


class FindTaskListsFilters(DTO):
    user_id: UUID
    name: str | None = None
