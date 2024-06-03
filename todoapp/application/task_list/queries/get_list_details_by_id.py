from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list.entities import TaskListDetails
from todoapp.domain.tasks_list.value_objects import ListId


@dataclass(frozen=True)
class GetListDetailsById(Query[TaskListDetails]):
    list_id: UUID


@dataclass
class GetListDetailsByIdHandler(QueryHandler[GetListDetailsById, TaskListDetails]):
    list_repo: TaskListRepo

    async def __call__(self, query: GetListDetailsById) -> TaskListDetails:
        list_id = ListId(query.list_id)
        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        return task_list
