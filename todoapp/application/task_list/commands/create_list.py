from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list.entities import TaskListDetails
from todoapp.domain.user.entities import UserId


@dataclass
class CreateTaskList(Command[TaskListDetails]):
    user_id: UUID
    name: str


class CreateTaskListHandler(CommandHandler[CreateTaskList, TaskListDetails]):
    uow: UnitOfWork
    list_repo: TaskListRepo

    async def __call__(self, command: CreateTaskList) -> TaskListDetails:
        user_id = UserId(command.user_id)
        task_list = TaskListDetails.create(command.name, user_id)
        await self.list_repo.add_task_list(task_list)
        await self.uow.commit()
        return task_list
