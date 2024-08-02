from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from todoapp.domain.common.exceptions import DomainError


@dataclass
class TaskAlreadyInList(DomainError):
    task_id: UUID
    list_id: UUID

    code: ClassVar[str] = "TASK_ALREADY_IN_LIST"

    @property
    def title(self) -> str:
        return f'The task with "{self.task_id}" task_id already in list with "{self.list_id}" list_id'


@dataclass(eq=False)
class SharingRuleNotExistsError(DomainError):
    list_id: UUID
    user_id: UUID

    code: ClassVar[str] = "SHARING_RULE_NOT_EXISTS"

    @property
    def title(self) -> str:
        return f'''Sharing for user "{self.user_id}" for list "{self.list_id}" doesn't exists'''


@dataclass(eq=False)
class TaskListVisibilityNotModified(DomainError):
    code: ClassVar[str] = "TASK_LIST_VISIBILITY_NOT_MODIFIED"

    @property
    def title(self) -> str:
        return "Visibility of a task list not modified"
