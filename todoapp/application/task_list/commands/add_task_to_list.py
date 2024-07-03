from dataclasses import dataclass
from uuid import UUID

from didiator import Mediator

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.application.task.queries import GetTaskById
from todoapp.application.task_list import dto
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass
class AddTaskToList(Command[dto.TaskList]):
    task_id: UUID
    user_id: UUID
    list_id: UUID


@dataclass
class AddTaskToListHandler(CommandHandler[AddTaskToList, dto.TaskList]):
    uow: UnitOfWork
    list_repo: TaskListRepo
    task_repo: TaskRepo
    mediator: Mediator

    async def __call__(self, command: AddTaskToList) -> dto.TaskList:
        user_id = UserId(command.user_id)

        task = await self.mediator.query(GetTaskById(
            command.task_id,
            command.user_id
        ))

        task_list = await self.list_repo.get_task_list_by_id(ListId(command.list_id))
        if not task_list.is_have_access(user_id):
            raise TaskListAccessError(command.list_id)

        task_list.add_task(task)

        await self.task_repo.update_task(task)
        await self.uow.commit()

        return dto.TaskList(
            id=task_list.id,
            user_id=task_list.user_id,
            name=task_list.name,
            created_at=task_list.created_at,
            tasks=task_list.tasks,
        )
