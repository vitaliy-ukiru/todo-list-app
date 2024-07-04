from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.user.entities import UserId


@dataclass
class CreateTaskList(Command[UUID]):
    user_id: UUID
    name: str


class CreateTaskListHandler(CommandHandler[CreateTaskList, TaskList]):
    uow: UnitOfWork
    list_repo: TaskListRepo

    async def __call__(self, command: CreateTaskList) -> UUID:
        user_id = UserId(command.user_id)
        task_list = TaskList.create(command.name, user_id)
        await self.list_repo.save_task_list(task_list)
        await self.uow.commit()
        return task_list.id
