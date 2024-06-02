from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from todoapp.application.common.pagination import Pagination
from todoapp.domain.tasks_list import entities
from todoapp.domain.tasks_list import value_objects as vo


class FindTaskListsFilters(BaseModel):
    user_id: UUID
    name: str | None = None
    include_deleted: bool = False


class TaskListRepo(Protocol):
    @abstractmethod
    async def add_task_list(self, task: entities.TaskList):
        raise NotImplementedError

    @abstractmethod
    async def acquire_task_list_by_id(self, list_id: vo.ListId) -> entities.TaskList:
        raise NotImplementedError

    @abstractmethod
    async def update_task_list(self, task: entities.TaskList):
        raise NotImplementedError

    @abstractmethod
    async def get_total_count(self, filters: FindTaskListsFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_task_lists(
        self,
        filters: FindTaskListsFilters,
        pagination: Pagination
    ) -> list[entities.TaskList]:
        raise NotImplementedError
