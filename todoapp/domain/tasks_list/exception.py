from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from todoapp.domain.common.exceptions import DomainError


@dataclass
class TaskInListConflict(DomainError):
    task_id: UUID
    list_id: UUID

    code: ClassVar[str] = "TASK_CONFLICT"

    @property
    def title(self) -> str:
        return f'''The task with "{self.task_id}" task_id don't belong to list "{self.list_id}" '''


@dataclass
class TaskAlreadyInList(DomainError):
    task_id: UUID
    list_id: UUID

    code: ClassVar[str] = "TASK_ALREADY_IN_LIST"

    @property
    def title(self) -> str:
        return f'The task with "{self.task_id}" task_id already in list with "{self.list_id}" list_id'


@dataclass
class TaskAlreadyInOtherList(DomainError):
    task_id: UUID
    list_id: UUID

    code: ClassVar[str] = "TASK_ALREADY_IN_OTHER_LIST"

    @property
    def title(self) -> str:
        return f'''The task with "{self.task_id}" task_id already in list "{self.list_id}"'''
