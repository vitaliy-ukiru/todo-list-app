from abc import abstractmethod
from typing import Protocol

from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.tasks_list.value_objects import ListId


class TaskListGetter(Protocol):
    @abstractmethod
    async def acquire_task_list_by_id(self, list_id: ListId) -> TaskList:
        raise NotImplementedError
