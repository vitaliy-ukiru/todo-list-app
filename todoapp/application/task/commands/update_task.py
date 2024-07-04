from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.domain.common.constants import Empty
from todoapp.domain.task.entities import Task
from todoapp.domain.task.value_objects import TaskId
from todoapp.domain.user.entities import UserId


@dataclass
class UpdateTask(Command[Task]):
    task_id: UUID
    user_id: UUID

    name: str | Empty = Empty.UNSET
    desc: str | None | Empty = Empty.UNSET


@dataclass
class UpdateTaskHandler(CommandHandler[UpdateTask, Task]):
    uow: UnitOfWork
    task_repo: TaskRepo

    async def __call__(self, command: UpdateTask) -> Task:
        task = await self.task_repo.acquire_task_by_id(TaskId(command.task_id))
        if not task.is_have_access(UserId(command.user_id)):
            raise TaskAccessError(command.task_id)

        if command.name is not Empty.UNSET:
            task.set_name(command.name)

        if command.desc is not Empty.UNSET:
            task.set_desc(command.desc)

        await self.task_repo.update_task(task)
        await self.uow.commit()

        return task
