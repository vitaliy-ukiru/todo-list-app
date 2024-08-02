from dataclasses import dataclass

from todoapp.application.common.pagination import Pagination, PaginationResult
from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.task_list.dto import FindTaskListsFilters, TaskListsDTO
from todoapp.application.task_list.interfaces import TaskListRepo


@dataclass(frozen=True)
class FindTaskLists(Query[TaskListsDTO]):
    filters: FindTaskListsFilters
    pagination: Pagination

@dataclass
class FindTaskListsHandler(QueryHandler[FindTaskLists, TaskListsDTO]):
    repo: TaskListRepo

    async def __call__(self, query: FindTaskLists) -> TaskListsDTO:
        lists = await self.repo.find_task_lists_details(
            filters=query.filters,
            pagination=query.pagination
        )
        total_count = await self.repo.get_total_count(query.filters)
        return TaskListsDTO(
            items=lists,
            pagination=PaginationResult.from_pagination(query.pagination, total_count)
        )
