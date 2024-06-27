from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from todoapp.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class UserIdAlreadyExistsError(ApplicationError):
    user_id: UUID

    code: ClassVar[str] = "USER_ID_ALREADY_EXISTS"

    @property
    def title(self) -> str:
        return f'A user with the "{self.user_id}" user_id already exists'


@dataclass(eq=False)
class UserIdNotExistError(ApplicationError):
    user_id: UUID

    code: ClassVar[str] = "USER_ID_NOT_FOUND"

    @property
    def title(self) -> str:
        return f"""A user with "{self.user_id}" user_id doesn't exist"""


@dataclass(eq=False)
class UserEmailNotExistError(ApplicationError):
    email: str

    code: ClassVar[str] = "USER_EMAIL_NOT_EXISTS"

    @property
    def title(self) -> str:
        return f"A user with \"{self.email}\" email doesn't exist"
