from dataclasses import dataclass
from typing import ClassVar

from todoapp.domain.common.exceptions import DomainError
from todoapp.domain.user.entities import UserId


@dataclass(eq=False)
class UserIsDeletedError(DomainError):
    user_id: UserId

    code: ClassVar[str] = "USER_DELETED"

    @property
    def title(self) -> str:
        return f'The user with "{self.user_id}" user_id is deleted'


@dataclass(eq=False)
class EmailAlreadyExistsError(DomainError):
    email: str | None = None

    code: ClassVar[str] = "USER_EMAIL_EXISTS"

    @property
    def title(self) -> str:
        if self.email is None:
            return "A user with the email already exists"
        return f'A user with the "{self.email}" email already exists'
