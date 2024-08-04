from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.access import Operation
from todoapp.domain.task_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass
class DeleteTaskList(Command[None]):
    list_id: UUID
    user_id: UUID


@dataclass
class DeleteTaskListHandler(CommandHandler[DeleteTaskList, None]):
    uow: UnitOfWork
    list_repo: TaskListRepo

    async def __call__(self, command: DeleteTaskList) -> None:
        user_id = UserId(command.user_id)
        list_id = ListId(command.list_id)

        task_list = await self.list_repo.acquire_task_list_by_id(list_id)
        if not task_list.is_have_access(user_id, Operation.delete_list):
            raise TaskListAccessError(list_id)

        await self.list_repo.delete_task_list(list_id)
        await self.uow.commit()
