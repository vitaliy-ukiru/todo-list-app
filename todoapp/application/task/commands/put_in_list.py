from dataclasses import dataclass
from uuid import UUID

from didiator import QueryMediator

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.queries import GetListById
from todoapp.domain.task.entities import Task, TaskId
from todoapp.domain.user.entities import UserId


@dataclass
class PutTaskInList(Command[Task]):
    task_id: UUID
    user_id: UUID
    list_id: UUID


@dataclass
class PutTaskInListHandler(CommandHandler[PutTaskInList, Task]):
    uow: UnitOfWork
    task_repo: TaskRepo
    mediator: QueryMediator

    async def __call__(self, command: PutTaskInList) -> Task:
        user_id = UserId(command.user_id)

        task = await self.task_repo.acquire_task_by_id(TaskId(command.task_id))
        if not task.is_have_access(user_id):
            raise TaskAccessError(command.task_id)

        task_list = await self.mediator.query(GetListById(list_id=command.list_id))
        if not task_list.is_have_access(user_id):
            raise TaskListAccessError(command.list_id)

        task.list_id = task_list.id

        await self.task_repo.update_task(task)
        await self.uow.commit()

        return task
