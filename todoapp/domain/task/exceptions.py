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
