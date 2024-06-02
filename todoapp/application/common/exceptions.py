from dataclasses import dataclass

from todoapp.domain.common.exceptions import AppError


class ApplicationError(AppError):
    """Base Application Exception."""

    @property
    def title(self) -> str:
        return "An application error occurred"


class UnexpectedError(ApplicationError):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass
