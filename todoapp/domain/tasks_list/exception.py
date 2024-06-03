from dataclasses import dataclass
from uuid import UUID

from todoapp.domain.common.exceptions import DomainError

@dataclass
class TaskInListConflict(DomainError):
    task_id: UUID
    list_id: UUID

    @property
    def title(self) -> str:
        return f'''The task with "{self.task_id}" task_id don't belong to list "{self.list_id}" '''


@dataclass
class TaskAlreadyInList(DomainError):
    task_id: UUID
    list_id: UUID
    @property
    def title(self) -> str:
        return f'The task with "{self.task_id}" task_id already in list with "{self.list_id}" list_id'


@dataclass
class TaskAlreadyInOtherList(DomainError):
    task_id: UUID
    list_id: UUID

    @property
    def title(self) -> str:
        return f'''The task with "{self.task_id}" task_id already in list "{self.list_id}"'''


