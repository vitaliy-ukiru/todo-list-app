from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.common.constants import Operation
from todoapp.domain.task_list.value_objects import ListId, SharingRule
from todoapp.domain.user.entities import UserId


@dataclass
class ShareTaskList(Command[None]):
    list_id: UUID
    user_id: UUID
    collaborator_id: UUID

    allow_update_tasks: bool = False
    allow_manage_tasks: bool = False


@dataclass
class ShareTaskListHandler(CommandHandler[ShareTaskList, None]):
    list_repo: TaskListRepo
    uow: UnitOfWork

    async def __call__(self, command: ShareTaskList) -> None:
        list_id = ListId(command.list_id)
        user_id = UserId(command.user_id)
        collaborator_id = UserId(command.collaborator_id)

        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        if not task_list.is_have_access(user_id, Operation.edit_sharing):
            raise TaskListAccessError(list_id)

        task_list.set_sharing_rule(collaborator_id, SharingRule(
            update_task_allowed=command.allow_update_tasks,
            manage_tasks_allowed=command.allow_manage_tasks,
        ))

        await self.list_repo.update_sharing_rules(task_list)
        await self.uow.commit()
