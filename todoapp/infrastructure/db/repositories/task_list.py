from typing import Iterable, NoReturn

from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.sql.functions import count

from todoapp.application.common.exceptions import RepoError
from todoapp.application.common.pagination import Pagination
from todoapp.application.task_list import dto
from todoapp.application.task_list.dto import FindTaskListsFilters
from todoapp.application.task_list.exceptions import TaskListAlreadyExistsError, TaskListNotExistsError, \
    SharingRuleNotExistsError
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.domain.tasks_list import entities
from todoapp.domain.tasks_list import value_objects as vo
from todoapp.domain.user.entities import UserId
from todoapp.infrastructure.db.models import TaskList, ListSharing
from .base import SQLAlchemyRepo
from .exception_mapper import exception_mapper


class TaskListRepoImpl(SQLAlchemyRepo, TaskListRepo):

    @exception_mapper
    async def save_task_list(self, task_list: entities.TaskList):
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

        sharing_rules = await self._get_sharing_rules(list_id)

        return convert_model_to_entity(task_list, sharing_rules)

    @exception_mapper
    async def update_task_list(self, task_list: entities.TaskList):
        model = convert_entity_to_model(task_list)
        try:
            await self._session.merge(model)
        except IntegrityError as err:
            self._parse_error(err, task_list)

    @exception_mapper
    async def delete_task_list(self, list_id: vo.ListId) -> None:
        task_list: TaskList | None = await self._session.get(
            TaskList, list_id,
        )
        if task_list is None:
            raise TaskListNotExistsError(list_id)

        await self._session.delete(task_list)
        await self._session.flush((task_list,))

    @exception_mapper
    async def get_total_count(self, filters: FindTaskListsFilters) -> int:
        query = select(count(TaskList.id))
        query = self._apply_filters(query, filters)
        items_count: int = await self._session.scalar(query)
        return items_count

    @exception_mapper
    async def find_task_lists_details(
        self,
        filters: FindTaskListsFilters,
        pagination: Pagination
    ) -> list[dto.TaskListDetails]:
        query = select(TaskList)
        query = self._apply_filters(query, filters)
        query = self.apply_pagination(query, pagination)
        result: Iterable[TaskList] = await self._session.scalars(query)
        lists = [convert_model_to_dto(task_list) for task_list in result]
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

        return query

    async def _get_sharing_rules(self, list_id: vo.ListId) -> list[ListSharing]:
        query = select(ListSharing).where(ListSharing.list_id == list_id)
        result: Iterable[ListSharing] = await self._session.scalars(query)
        return list(result)

    @exception_mapper
    async def share_task_list(self, list_id: vo.ListId, user_id: UserId, rule: vo.SharingRule):
        sharing = ListSharing(
            list_id=list_id,
            user_id=user_id,
            update_tasks=rule.update_task_allowed,
            manage_task=rule.manage_tasks_allowed
        )

        await self._session.merge(sharing)

    @exception_mapper
    async def delete_share(self, list_id: vo.ListId, user_id: UserId):
        sharing: ListSharing | None = await self._session.get(
            TaskList, (list_id, user_id)
        )
        if sharing is None:
            raise SharingRuleNotExistsError(list_id, user_id)

        await self._session.delete(sharing)
        await self._session.flush((sharing,))


def convert_entity_to_model(task_list: entities.TaskList) -> TaskList:
    return TaskList(
        id=task_list.id,
        name=task_list.name,
        user_id=task_list.user_id,
        created_at=task_list.created_at,
        public=task_list.sharing.public,
    )


def convert_sharing_rule(rule: ListSharing) -> vo.SharingRule:
    return vo.SharingRule(
        update_task_allowed=rule.update_tasks,
        manage_tasks_allowed=rule.manage_task,
    )


def convert_model_to_entity(task_list: TaskList, sharing_rules: list[ListSharing]) -> entities.TaskList:
    return entities.TaskList(
        id=vo.ListId(task_list.id),
        name=task_list.name,
        user_id=UserId(task_list.user_id),
        created_at=task_list.created_at,
        sharing=vo.Sharing(
            public=task_list.public,
            collaborators={
                UserId(rule.user_id): convert_sharing_rule(rule)
                for rule in sharing_rules
            }
        )
    )


def convert_model_to_dto(task_list: TaskList) -> dto.TaskListDetails:
    return dto.TaskListDetails(
        id=task_list.id,
        name=task_list.name,
        user_id=task_list.user_id,
        created_at=task_list.created_at,
        public=task_list.public
    )
