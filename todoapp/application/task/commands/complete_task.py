from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.domain.task.entities import Task, TaskId
from todoapp.domain.user.entities import UserId


@dataclass
class CompleteTask(Command[Task]):
    task_id: UUID
    user_id: UUID


@dataclass
class CompleteTaskHandler(CommandHandler[CompleteTask, Task]):
    uow: UnitOfWork
    task_repo: TaskRepo

    async def __call__(self, command: CompleteTask) -> Task:
        task = await self.task_repo.acquire_task_by_id(TaskId(command.task_id))
        if not task.is_have_access(UserId(command.user_id)):
            raise TaskAccessError(command.task_id)

        task.complete()
        await self.task_repo.update_task(task)
        await self.uow.commit()

        return task
