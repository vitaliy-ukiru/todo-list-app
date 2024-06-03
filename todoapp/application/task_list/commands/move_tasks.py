from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.application.task_list.interfaces.task_mover import TaskMover
from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId


@dataclass
class MoveTasks(Command[TaskList]):
    user_id: UUID
    from_list: UUID
    to_list: UUID


@dataclass
class MoveTasksHandler(CommandHandler[MoveTasks, TaskList]):
    list_repo: TaskListRepo
    task_mover: TaskMover
    uow: UnitOfWork

    async def __call__(self, command: MoveTasks) -> TaskList:
        user_id = UserId(command.user_id)
        from_list_id = ListId(command.from_list)
        to_list_id = ListId(command.to_list)

        from_list = await self.list_repo.get_task_list_by_id(from_list_id)
        if not from_list.is_have_access(user_id):
            raise TaskListAccessError(command.from_list)

        dest_list = await self.list_repo.get_task_list_by_id(to_list_id)

        from_list.move_tasks_another_list(dest_list)
        await self.task_mover.move_task_between_lists(from_list_id, to_list_id)
        await self.uow.commit()

        return dest_list
