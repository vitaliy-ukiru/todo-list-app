from dataclasses import dataclass
from uuid import UUID

from didiator import Mediator

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.queries import GetListDetailsById
from todoapp.domain.task.entities import Task
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass
class CreateTask(Command[UUID]):
    user_id: UUID
    name: str
    desc: str | None = None
    list_id: UUID | None = None


@dataclass
class CreateTaskHandler(CommandHandler[CreateTask, UUID]):
    uow: UnitOfWork
    task_repo: TaskRepo
    mediator: Mediator

    async def _check_list_owner(self, list_id: UUID, user_id: UserId):
        task_list = await self.mediator.query(GetListDetailsById(
            list_id=list_id
        ))
        if task_list.is_have_access(user_id):
            raise TaskListAccessError(list_id)

    async def __call__(self, command: CreateTask) -> UUID:
        user_id = UserId(command.user_id)
        if command.list_id is not None:
            await self._check_list_owner(command.list_id, user_id)

        task = Task.create(
            command.name,
            user_id,
            command.desc,
            ListId(command.list_id) if command.list_id else None
        )
        await self.task_repo.add_task(task)
        await self.uow.commit()

        return task.id
