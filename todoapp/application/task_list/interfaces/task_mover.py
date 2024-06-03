from abc import abstractmethod
from typing import Protocol

from todoapp.domain.tasks_list.value_objects import ListId


class TaskMover(Protocol):
    @abstractmethod
    async def move_task_between_lists(
        self,
        from_list: ListId,
        to_list: ListId
    ) -> None:
        raise NotImplementedError
