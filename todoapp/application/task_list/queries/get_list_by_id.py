from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task_list import dto
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo,TaskInListFinder
from todoapp.domain.access import Operation
from todoapp.domain.task_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass(frozen=True)
class GetListById(Query[dto.TaskList]):
    list_id: UUID
    user_id: UUID


@dataclass
class GetListByIdHandler(QueryHandler[GetListById, dto.TaskList]):
    list_repo: TaskListRepo
    tasks_finder: TaskInListFinder

    async def __call__(self, query: GetListById) -> dto.TaskList:
        list_id = ListId(query.list_id)
        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        if not task_list.is_have_access(UserId(query.user_id), Operation.read):
            raise TaskListAccessError(query.list_id)

        tasks = await self.tasks_finder.get_tasks_in_list(list_id)
        return dto.TaskList.from_entity(task_list, tasks)
