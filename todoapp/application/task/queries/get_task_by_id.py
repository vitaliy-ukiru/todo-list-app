from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task.dto import Task
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.domain.common.constants import Operation
from todoapp.domain.task.value_objects import TaskId
from todoapp.domain.user.entities import UserId


@dataclass
class GetTaskById(Query[Task]):
    task_id: UUID
    user_id: UUID


@dataclass
class GetTaskByIdHandler(QueryHandler[GetTaskById, Task]):
    task_repo: TaskRepo

    async def __call__(self, query: GetTaskById) -> Task:
        task_id = TaskId(query.task_id)
        task = await self.task_repo.acquire_task_by_id(task_id)
        if not task.is_have_access(UserId(query.user_id), Operation.read):
            raise TaskAccessError(task_id)

        return Task.from_entity(task)
