from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task_list import dto
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.task_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass(frozen=True)
class GetListSharingById(Query[dto.TaskListSharing]):
    list_id: UUID
    user_id: UUID


@dataclass
class GetListSharingByIdHandler(QueryHandler[GetListSharingById, dto.TaskListSharing]):
    list_repo: TaskListRepo

    async def __call__(self, query: GetListSharingById) -> dto.TaskListSharing:
        list_id = ListId(query.list_id)
        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        user_id = UserId(query.user_id)

        is_owner = task_list.user_id == user_id
        is_collaborator = user_id in task_list.sharing.collaborators
        if not (is_owner or is_collaborator):
            raise TaskListAccessError(query.list_id)

        return dto.TaskListSharing.from_entity(task_list)
