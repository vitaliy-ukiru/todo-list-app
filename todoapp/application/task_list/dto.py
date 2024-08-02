from datetime import datetime
from typing import TypeAlias, Self
from uuid import UUID

from todoapp.application.common.dto import DTO
from todoapp.application.common.pagination import PaginatedItemsDTO
from todoapp.application.task.dto import Task as TaskDTO
from todoapp.domain.task_list import entities
from todoapp.domain.task_list.value_objects import SharingRule


class BaseTaskList(DTO):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime
    public: bool

    @classmethod
    def from_entity(cls, entity: entities.TaskList) -> Self:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            created_at=entity.created_at,
            public=entity.sharing.public,
        )


TaskListsDTO: TypeAlias = PaginatedItemsDTO[BaseTaskList]


class TaskList(DTO):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime
    public: bool
    tasks: list[TaskDTO]

    @classmethod
    def from_entity(cls, entity: entities.TaskList, tasks: list[TaskDTO]) -> Self:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            created_at=entity.created_at,
            tasks=tasks,
            public=entity.sharing.public
        )


class TaskListSharing(BaseTaskList):
    sharing: dict[UUID, SharingRule]

    @classmethod
    def from_entity(cls, entity: entities.TaskList) -> Self:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            created_at=entity.created_at,
            public=entity.sharing.public,
            sharing=entity.sharing.collaborators,
        )


class FindTaskListsFilters(DTO):
    user_id: UUID
    name: str | None = None
