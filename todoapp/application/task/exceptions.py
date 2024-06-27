from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from todoapp.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class TaskAlreadyExistsError(ApplicationError):
    task_id: UUID

    code: ClassVar[str] = "TASK_ALREADY_EXISTS"

    @property
    def title(self) -> str:
        return f'A task with the "{self.task_id}" task_id already exists'


@dataclass(eq=False)
class TaskNotExistsError(ApplicationError):
    task_id: UUID

    code: ClassVar[str] = "TASK_NOT_EXISTS"

    @property
    def title(self) -> str:
        return f'''A task with the "{self.task_id}" task_id doesn't exists'''


@dataclass(eq=False)
class TaskAccessError(ApplicationError):
    task_id: UUID

    code: ClassVar[str] = "TASK_ACCESS_DENIED"

    @property
    def title(self) -> str:
        return f"You don't have access to task \"{self.task_id}\""
