from abc import abstractmethod
from typing import Protocol

from todoapp.application.common.pagination import Pagination
from todoapp.application.task_list import dto
from todoapp.application.task_list.dto import FindTaskListsFilters
from todoapp.domain.tasks_list import entities
from todoapp.domain.tasks_list import value_objects as vo


class TaskListRepo(Protocol):
    @abstractmethod
    async def add_task_list(self, task: entities.TaskListDetails):
        raise NotImplementedError

    @abstractmethod
    async def acquire_task_list_by_id(self, list_id: vo.ListId) -> entities.TaskListDetails:
        raise NotImplementedError

    @abstractmethod
    async def update_task_list(self, task: entities.TaskListDetails):
        raise NotImplementedError

    @abstractmethod
    async def get_total_count(self, filters: FindTaskListsFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_task_lists_details(
        self,
        filters: FindTaskListsFilters,
        pagination: Pagination
    ) -> list[dto.TaskListDetails]:
        raise NotImplementedError

    @abstractmethod
    async def get_task_list_by_id(self, list_id: vo.ListId) -> entities.TaskList:
        raise NotImplementedError

    @abstractmethod
    async def delete_task_list(self, list_id: vo.ListId) -> None:
        raise NotImplementedError
