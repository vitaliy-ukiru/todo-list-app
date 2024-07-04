from dataclasses import dataclass
from uuid import UUID

from didiator import QueryMediator

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.dto import Task
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.interfaces import TaskRepo,TaskListGetter
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.domain.common.constants import Operation
from todoapp.domain.task.value_objects import TaskId
from todoapp.domain.tasks_list.value_objects import ListId
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
    list_repo: TaskListGetter
    mediator: QueryMediator

    async def __call__(self, command: PutTaskInList) -> Task:
        user_id = UserId(command.user_id)

        task = await self.task_repo.acquire_task_by_id(TaskId(command.task_id))
        if not task.is_have_access(user_id, Operation.update_task):
            raise TaskAccessError(command.task_id)

        task_list = await self.list_repo.acquire_task_list_by_id(ListId(command.list_id))

        # check that issuer can add task to target list
        if not task_list.is_have_access(user_id, Operation.add_task_to_list):
            raise TaskListAccessError(command.list_id)

        # check that issuer can delete task from source list
        if task.list and not task.list.is_have_access(user_id, Operation.delete_task_from_list):
            raise TaskListAccessError(task.list.id)

        task.set_list(task_list)

        await self.task_repo.update_task(task)
        await self.uow.commit()

        return Task.from_entity(task)
