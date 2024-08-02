from abc import abstractmethod
from typing import Protocol

from todoapp.domain.task_list.entities import TaskList
from todoapp.domain.task_list.value_objects import ListId


class TaskListGetter(Protocol):
    @abstractmethod
    async def acquire_task_list_by_id(self, list_id: ListId) -> TaskList:
        raise NotImplementedError
