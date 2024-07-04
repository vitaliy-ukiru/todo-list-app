from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.common.constants import Operation
from todoapp.domain.tasks_list.value_objects import ListId, SharingRule
from todoapp.domain.user.entities import UserId


@dataclass
class ShareTaskList(Command[None]):
    list_id: UUID
    user_id: UUID

    allow_update_tasks: bool = False
    allow_manage_tasks: bool = False


@dataclass
class ShareTaskListHandler(CommandHandler[ShareTaskList, None]):
    list_repo: TaskListRepo
    uow: UnitOfWork

    async def __call__(self, command: ShareTaskList) -> None:
        list_id = ListId(command.list_id)
        user_id = UserId(command.user_id)

        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        if not task_list.is_have_access(user_id, Operation.edit_sharing):
            raise TaskListAccessError(list_id)

        await self.list_repo.share_task_list(
            list_id,
            user_id,
            SharingRule(
                update_task_allowed=command.allow_update_tasks,
                manage_tasks_allowed=command.allow_manage_tasks,
            )
        )
        await self.uow.commit()
