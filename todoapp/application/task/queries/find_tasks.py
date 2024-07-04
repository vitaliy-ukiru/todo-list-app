from dataclasses import dataclass

from todoapp.application.common.pagination import Pagination, PaginationResult
from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task.dto import TasksDTO, FindTasksFilters
from todoapp.application.task.interfaces import TaskRepo


@dataclass(frozen=True)
class FindTasks(Query[list[TasksDTO]]):
    filters: FindTasksFilters
    pagination: Pagination


@dataclass
class FindTasksHandler(QueryHandler[FindTasks, TasksDTO]):
    task_repo: TaskRepo

    async def __call__(self, query: FindTasks) -> TasksDTO:
        tasks = await self.task_repo.find_tasks(query.filters, query.pagination)
        total_count = await self.task_repo.get_total_count(query.filters)
        return TasksDTO(
            items=tasks,
            pagination=PaginationResult.from_pagination(query.pagination, total_count)
        )
