from typing import ClassVar

from todoapp.domain.common.exceptions import DomainError


class TaskNameOutOfRange(DomainError):
    code: ClassVar[str] = "TASK_NAME_OUT_OF_RANGE"

    def title(self) -> str:
        return "Length of task's name must be between 3 and 500"


class TaskDescOutOfRange(DomainError):
    code: ClassVar[str] = "TASK_DESC_OUT_OF_RANGE"

    def title(self) -> str:
        return "Length of task's desc must be between 3 and 500"


class MoveTaskToRestrictedList(DomainError):
    code: ClassVar[str] = "MOVE_TASK_TO_RESTRICT_LIST"

    def title(self) -> str:
        return "Moving a task to a list that is closed to the task author is restricted"
