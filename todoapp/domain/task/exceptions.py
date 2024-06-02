from todoapp.domain.common.exceptions import DomainError


class TaskNameOutOfRange(DomainError):
    def title(self) -> str:
        return "Length of task's name must be between 3 and 500"


class TaskDescOutOfRange(DomainError):
    def title(self) -> str:
        return "Length of task's desc must be between 3 and 500"
