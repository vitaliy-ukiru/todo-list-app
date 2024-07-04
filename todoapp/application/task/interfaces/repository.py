from abc import abstractmethod
from typing import Protocol

from todoapp.application.common.pagination import Pagination
from todoapp.application.task import dto
from todoapp.domain.task.entities import Task
from todoapp.domain.task.value_objects import TaskId
from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.tasks_list.value_objects import ListId


class TaskRepo(Protocol):
    @abstractmethod
    async def add_task(self, task: Task):
        raise NotImplementedError

    @abstractmethod
    async def acquire_task_by_id(self, task_id: TaskId) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task):
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: TaskId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_total_count(self, filters: dto.FindTasksFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_tasks(
        self,
        filters: dto.FindTasksFilters,
        pagination: Pagination
    ) -> list[dto.Task]:
        raise NotImplementedError


class TaskListGetter(Protocol):
    @abstractmethod
    async def acquire_task_list_by_id(self, list_id: ListId) -> TaskList:
        raise NotImplementedError
