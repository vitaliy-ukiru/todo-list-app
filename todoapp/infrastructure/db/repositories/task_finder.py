from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select

from todoapp.application.task import dto
from todoapp.application.task_list.interfaces.task_finder import TaskInListFinder
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.infrastructure.db.models import Task
from .base import SQLAlchemyRepo
from .task import convert_model_to_dto


@dataclass
class TaskInListFinderImpl(SQLAlchemyRepo, TaskInListFinder):

    async def get_tasks_in_list(self, list_id: ListId) -> list[dto.Task]:
        query = select(Task).where(Task.list_id == list_id)
        result: Iterable[Task] = await self._session.scalars(query)
        tasks = [convert_model_to_dto(task) for task in result]
        return tasks
