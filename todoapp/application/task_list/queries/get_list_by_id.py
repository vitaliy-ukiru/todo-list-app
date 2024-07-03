from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task_list import dto
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass(frozen=True)
class GetListById(Query[dto.TaskList]):
    list_id: UUID
    user_id: UUID


@dataclass
class GetListByIdHandler(QueryHandler[GetListById, dto.TaskList]):
    list_repo: TaskListRepo

    async def __call__(self, query: GetListById) -> dto.TaskListDetails:
        list_id = ListId(query.list_id)
        task_list = await self.list_repo.get_task_list_by_id(list_id)
        if not task_list.is_have_access(UserId(query.user_id)):
            raise TaskListAccessError(query.list_id)

        return dto.TaskList(
            id=task_list.id,
            user_id=task_list.user_id,
            name=task_list.name,
            created_at=task_list.created_at,
            tasks=task_list.tasks,
        )

