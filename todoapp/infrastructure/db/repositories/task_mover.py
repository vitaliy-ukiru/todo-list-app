from sqlalchemy import update

from todoapp.application.task_list.interfaces.task_mover import TaskMover
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.infrastructure.db.models import Task
from todoapp.infrastructure.db.repositories.base import SQLAlchemyRepo


class TaskMoverImpl(SQLAlchemyRepo, TaskMover):

    async def move_task_between_lists(
        self,
        from_list: ListId,
        to_list: ListId
    ) -> None:
        query = (
            update(Task).
            values(list_id=to_list).
            where(Task.list_id == from_list)
        )

        await self._session.execute(query)
