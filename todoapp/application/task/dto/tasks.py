from typing import TypeAlias

from todoapp.application.common.pagination import PaginatedItemsDTO
from todoapp.domain.task.entities import Task

TasksDTO: TypeAlias = PaginatedItemsDTO[Task]