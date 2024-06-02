from typing import Iterable, NoReturn

from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.sql.functions import count

from todoapp.application.common.exceptions import RepoError
from todoapp.application.common.pagination import Pagination
from todoapp.application.task_list.exceptions import TaskListAlreadyExistsError, TaskListNotExistsError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.application.task_list.interfaces.repository import FindTaskListsFilters
from todoapp.domain.tasks_list import entities
from todoapp.domain.tasks_list import value_objects as vo
from todoapp.domain.user.entities import UserId
from todoapp.infrastructure.db.models import TaskList
from todoapp.infrastructure.db.repositories.base import SQLAlchemyRepo
from todoapp.infrastructure.db.repositories.exception_mapper import exception_mapper


class TaskListRepoImpl(SQLAlchemyRepo, TaskListRepo):
    @exception_mapper
    async def add_task_list(self, task_list: entities.TaskList):
        model = convert_entity_to_model(task_list)
        self._session.add(model)
        try:
            await self._session.flush((model,))
        except IntegrityError as err:
            self._parse_error(err, task_list)

    @exception_mapper
    async def acquire_task_list_by_id(self, list_id: vo.ListId) -> entities.TaskList:
        task_list: TaskList | None = await self._session.get(TaskList, list_id)
        if task_list is None:
            raise TaskListNotExistsError(list_id)

        return convert_model_to_entity(task_list)

    @exception_mapper
    async def update_task_list(self, task_list: entities.TaskList):
        model = convert_model_to_entity(task_list)
        try:
            await self._session.merge(model)
        except IntegrityError as err:
            self._parse_error(err, task_list)

    @exception_mapper
    async def get_total_count(self, filters: FindTaskListsFilters) -> int:
        query = select(count(TaskList.id))
        query = self._apply_filters(query, filters)
        items_count: int = await self._session.scalar(query)
        return items_count

    @exception_mapper
    async def find_task_lists(
        self,
        filters: FindTaskListsFilters,
        pagination: Pagination
    ) -> list[entities.TaskList]:
        query = select(TaskList)
        query = self._apply_filters(query, filters)
        query = self.apply_pagination(query, pagination)
        result: Iterable[TaskList] = await self._session.scalars(query)
        lists = [convert_model_to_entity(task_list) for task_list in result]
        return lists

    @staticmethod
    def _parse_error(err: DBAPIError, task: entities.TaskList) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "task_lists_pkey":
                raise TaskListAlreadyExistsError(task.id) from err
            case _:
                raise RepoError from err

    @staticmethod
    def _apply_filters(query: Select, filters: FindTaskListsFilters) -> Select:
        query = query.where(TaskList.user_id == filters.user_id)
        if filters.user_id is not None:
            query = query.where(TaskList.name.icontains(filters.user_id))

        if not filters.include_deleted:
            query = query.where(TaskList.deleted_at.is_not(None))

        return query


def convert_entity_to_model(task_list: entities.TaskList) -> TaskList:
    return TaskList(
        id=task_list.id,
        name=task_list.name,
        user_id=task_list.user_id,
        created_at=task_list.created_at,
        deleted_at=task_list.deleted_at,
    )


def convert_model_to_entity(task_list: TaskList) -> entities.TaskList:
    return entities.TaskList(
        id=task_list.id,
        name=task_list.name,
        user_id=UserId(task_list.user_id),
        created_at=task_list.created_at,
        deleted_at=task_list.deleted_at
    )
