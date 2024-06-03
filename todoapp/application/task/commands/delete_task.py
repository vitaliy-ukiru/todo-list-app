from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.domain.task.entities import TaskId
from todoapp.domain.user.entities import UserId


@dataclass
class DeleteTask(Command[None]):
    task_id: UUID
    user_id: UUID


@dataclass
class DeleteTaskHandler(CommandHandler[DeleteTask, None]):
    uow: UnitOfWork
    task_repo: TaskRepo

    async def __call__(self, command: DeleteTask) -> None:
        user_id = UserId(command.user_id)
        task_id = TaskId(command.task_id)

        task = await self.task_repo.acquire_task_by_id(task_id)
        if not task.is_have_access(user_id):
            raise TaskAccessError(command.task_id)

        await self.task_repo.delete_task(task_id)

