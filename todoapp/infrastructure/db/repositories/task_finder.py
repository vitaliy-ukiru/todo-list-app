from dataclasses import dataclass

from todoapp.application.common.pagination import Pagination
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.application.task.dto.tasks import FindTasksFilters
from todoapp.domain.task.entities import Task
from todoapp.domain.tasks_list import value_objects as vo
from .task_list import TaskInListFinder


@dataclass
class TaskInListFinderImpl(TaskInListFinder):
    task_repo: TaskRepo

    async def get_tasks_in_list(self, list_id: vo.ListId) -> list[Task]:
        tasks = await self.task_repo.find_tasks(FindTasksFilters(
            list_id=list_id
        ), Pagination())

        return tasks
