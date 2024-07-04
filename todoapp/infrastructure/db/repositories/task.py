from typing import NoReturn, Iterable

from sqlalchemy import select, Select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from todoapp.application.common.exceptions import RepoError
from todoapp.application.common.pagination import Pagination, SortOrder
from todoapp.application.task import dto
from todoapp.application.task.exceptions import TaskAlreadyExistsError, TaskNotExistsError
from todoapp.application.task.interfaces.repository import TaskRepo, TaskListGetter
from todoapp.domain.common.constants import Empty
from todoapp.domain.task import entities
from todoapp.domain.task.value_objects import TaskId
from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import UserId
from todoapp.infrastructure.db.models import Task
from todoapp.infrastructure.db.repositories.base import SQLAlchemyRepo
from .exception_mapper import exception_mapper


class TaskRepoImpl(SQLAlchemyRepo, TaskRepo):
    def __init__(self, session: AsyncSession, list_getter: TaskListGetter):
        self._list_getter = list_getter
        super().__init__(session)

    @exception_mapper
    async def add_task(self, task: entities.Task):
        db_task = convert_entity_to_model(task)
        self._session.add(db_task)
        try:
            await self._session.flush((db_task,))
        except IntegrityError as err:
            self._parse_error(err, task)

    @exception_mapper
    async def acquire_task_by_id(self, task_id: TaskId) -> entities.Task:
        task: Task | None = await self._session.get(
            Task,
            task_id,
            with_for_update=True
        )
        if task is None:
            raise TaskNotExistsError(task_id)

        task_list = None
        if task.list_id is not None:
            task_list = await self._list_getter.acquire_task_list_by_id(ListId(task.list_id))

        return convert_model_to_entity(task, task_list)

    @exception_mapper
    async def update_task(self, task: entities.Task):
        model = convert_entity_to_model(task)
        try:
            await self._session.merge(model)
        except IntegrityError as err:
            self._parse_error(err, task)

    @exception_mapper
    async def delete_task(self, task_id: TaskId) -> None:
        task: Task | None = await self._session.get(
            Task, task_id,
        )
        if task is None:
            raise TaskNotExistsError(task_id)

        await self._session.delete(task)
        await self._session.flush((task,))

    @exception_mapper
    async def find_tasks(
        self,
        filters: dto.FindTasksFilters,
        pagination: Pagination
    ) -> list[entities.Task]:
        query = select(Task)
        if pagination.order is SortOrder.ASC:
            query = query.order_by(Task.id.asc())
        else:
            query = query.order_by(Task.id.desc())

        query = self._apply_filters(query, filters)
        query = self.apply_pagination(query, pagination)

        result: Iterable[Task] = await self._session.scalars(query)
        tasks = [convert_model_to_dto(task) for task in result]
        return tasks

    @exception_mapper
    async def get_total_count(self, filters: dto.FindTasksFilters) -> int:
        query = select(count(Task.id))
        query = self._apply_filters(query, filters)
        tasks_count: int = await self._session.scalar(query)
        return tasks_count

    @staticmethod
    def _parse_error(err: DBAPIError, task: entities.Task) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "tasks_pkey":
                raise TaskAlreadyExistsError(task.id) from err
            case _:
                raise RepoError from err

    @staticmethod
    def _apply_filters(query: Select, filters: dto.FindTasksFilters) -> Select:
        query = query.where(Task.user_id == filters.user_id)

        if filters.name:
            query = query.where(Task.name.icontains(filters.name))

        if filters.desc:
            query = query.where(Task.desc.icontains(filters.desc))

        if filters.completed is not Empty.UNSET:
            query = query.where(
                Task.done_at.is_not(None) if filters.completed else Task.done_at.is_(None)
            )

        if filters.list_id is not Empty.UNSET:
            if filters.list_id is None:
                query = query.where(Task.list_id.is_(None))
            else:
                query = query.where(Task.list_id == filters.list_id)  # type: ignore

        return query


def convert_entity_to_model(task: entities.Task) -> Task:
    return Task(
        id=task.id,
        name=task.name,
        desc=task.desc,
        done_at=task.completed_at,
        user_id=task.user_id,
        list_id=task.list.id if task.list else None,
        created_at=task.created_at,
    )


def convert_model_to_dto(task: Task) -> dto.Task:
    return dto.Task(
        id=task.id,
        name=task.name,
        desc=task.desc,
        completed_at=task.done_at,
        user_id=task.user_id,
        list_id=task.list_id,
        created_at=task.created_at
    )


def convert_model_to_entity(task: Task, task_list: TaskList | None) -> entities.Task:
    return entities.Task(
        id=task.id,
        name=task.name,
        desc=task.desc,
        completed_at=task.done_at,
        user_id=UserId(task.user_id),
        list=task_list,
        created_at=task.created_at
    )
