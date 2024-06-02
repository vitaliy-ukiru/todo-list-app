from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from todoapp.application.common.pagination import Pagination
from todoapp.domain.common.constants import Empty
from todoapp.domain.task.entities import Task, TaskId


class FindTasksFilters(BaseModel):
    name: str | None = None
    desc: str | None = None
    completed: bool | Empty = Empty.UNSET
    list_id: UUID | None | Empty = Empty.UNSET


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
    async def get_total_count(self, filters: FindTasksFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_tasks(self, filters: FindTasksFilters, pagination: Pagination) -> list[Task]:
        raise NotImplementedError
