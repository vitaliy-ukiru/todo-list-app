from abc import abstractmethod
from typing import Protocol

from todoapp.application.task.dto import Task as TaskDTO
from todoapp.domain.task_list.value_objects import ListId


class TaskInListFinder(Protocol):
    @abstractmethod
    async def get_tasks_in_list(self, list_id: ListId) -> list[TaskDTO]:
        raise NotImplementedError
