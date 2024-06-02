from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.domain.task.entities import Task, TaskId
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
        if not task.is_have_access(UserId(query.user_id)):
            raise TaskAccessError(task_id)

        return task
