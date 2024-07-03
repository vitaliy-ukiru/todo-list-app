from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass(frozen=True)
class GetListById(Query[TaskList]):
    list_id: UUID
    user_id: UUID


@dataclass
class GetListByIdHandler(QueryHandler[GetListById, TaskList]):
    list_repo: TaskListRepo

    async def __call__(self, query: GetListById) -> TaskList:
        list_id = ListId(query.list_id)
        task_list = await self.list_repo.get_task_list_by_id(list_id)
        if not task_list.is_have_access(UserId(query.user_id)):
            raise TaskListAccessError(query.list_id)

        return task_list
