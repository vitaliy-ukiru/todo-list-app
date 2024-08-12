from dataclasses import dataclass
from uuid import UUID

from didiator import Mediator

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.interfaces import TaskRepo,TaskListGetter
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.domain.access import Operation
from todoapp.domain.task.entities import Task
from todoapp.domain.task_list.value_objects import ListId
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
    list_repo: TaskListGetter
    mediator: Mediator

    async def __call__(self, command: CreateTask) -> UUID:
        user_id = UserId(command.user_id)
        list_id = ListId(command.list_id)
        task_list = None
        if command.list_id is not None:
            task_list = await self.list_repo.acquire_task_list_by_id(list_id)

        task = Task.create(
            command.name,
            user_id,
            command.desc,
            task_list,
        )
        await self.task_repo.add_task(task)
        await self.uow.commit()

        return task.id
