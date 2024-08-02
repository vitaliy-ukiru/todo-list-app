from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.common.constants import Operation
from todoapp.domain.task_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass
class ChangeVisibility(Command[None]):
    list_id: UUID
    user_id: UUID
    public: bool


@dataclass
class ChangeVisibilityHandler(CommandHandler[ChangeVisibility, None]):
    list_repo: TaskListRepo
    uow: UnitOfWork

    async def __call__(self, command: ChangeVisibility) -> None:
        list_id = ListId(command.list_id)
        user_id = UserId(command.user_id)

        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        if not task_list.is_have_access(user_id, Operation.edit_sharing):
            raise TaskListAccessError(list_id)

        task_list.change_visibility(command.public)

        await self.list_repo.update_task_list(task_list)
        await self.uow.commit()
