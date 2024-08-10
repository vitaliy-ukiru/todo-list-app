from dataclasses import dataclass

from todoapp.application.common.pagination import Pagination, PaginationResult
from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task.dto import TasksDTO, FindTasksFilters
from todoapp.application.task.interfaces import TaskRepo
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.access import Operation
from todoapp.domain.common.constants import Empty
from todoapp.domain.task_list.value_objects import ListId


@dataclass(frozen=True)
class FindTasks(Query[list[TasksDTO]]):
    filters: FindTasksFilters
    pagination: Pagination


@dataclass
class FindTasksHandler(QueryHandler[FindTasks, TasksDTO]):
    task_repo: TaskRepo
    list_repo: TaskListRepo

    async def __call__(self, query: FindTasks) -> TasksDTO:
        if query.filters.list_id and query.filters.list_id is not Empty.UNSET:
            task_list = await self.list_repo.acquire_task_list_by_id(ListId(query.filters.list_id))
            if not task_list.is_have_access(query.filters.user_id, Operation.read):
                raise TaskListAccessError(query.filters.list_id)

        tasks = await self.task_repo.find_tasks(query.filters, query.pagination)
        total_count = await self.task_repo.get_total_count(query.filters)
        return TasksDTO(
            items=tasks,
            pagination=PaginationResult.from_pagination(query.pagination, total_count)
        )
