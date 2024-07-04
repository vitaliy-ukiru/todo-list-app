from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from todoapp.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class TaskListAlreadyExistsError(ApplicationError):
    task_list_id: UUID

    code: ClassVar[str] = "TASK_LIST_ALREADY_EXISTS"

    @property
    def title(self) -> str:
        return f'A task list with the "{self.task_list_id}" id already exists'


@dataclass(eq=False)
class TaskListNotExistsError(ApplicationError):
    task_list_id: UUID

    code: ClassVar[str] = "TASK_LIST_NOT_EXISTS"

    @property
    def title(self) -> str:
        return f'''A task list with the "{self.task_list_id}" id doesn't exists'''


@dataclass(eq=False)
class SharingRuleNotExistsError(ApplicationError):
    list_id: UUID
    user_id: UUID

    code: ClassVar[str] = "SHARING_RULE_NOT_EXISTS"

    @property
    def title(self) -> str:
        return f'''Sharing for user "{self.user_id}" for list "{self.list_id}" doesn't exists'''


@dataclass(eq=False)
class TaskListAccessError(ApplicationError):
    task_list_id: UUID

    code: ClassVar[str] = "TASK_LIST_ACCESS_DENIED"

    @property
    def title(self) -> str:
        return f"You don't have access to task list \"{self.task_list_id}\""


@dataclass(eq=False)
class TaskListVisibilityNotModified(ApplicationError):
    code: ClassVar[str] = "TASK_LIST_VISIBILITY_NOT_MODIFIED"


    @property
    def title(self) -> str:
        return "Visibility of a task list not modified"
