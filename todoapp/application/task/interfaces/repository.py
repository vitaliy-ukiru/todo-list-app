from abc import abstractmethod
from typing import Protocol

from todoapp.application.common.pagination import Pagination
from todoapp.application.task.dto.tasks import FindTasksFilters
from todoapp.domain.task.entities import Task
from todoapp.domain.task.value_objects import TaskId


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
    async def get_total_count(self, filters: FindTasksFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_tasks(self, filters: FindTasksFilters, pagination: Pagination) -> list[Task]:
        raise NotImplementedError
