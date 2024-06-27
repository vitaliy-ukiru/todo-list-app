from dataclasses import dataclass
from typing import ClassVar

from todoapp.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class RefreshTokenNotFound(ApplicationError):
    code: ClassVar[str] = "REFRESH_TOKEN_NOT_FOUND"

    @property
    def title(self) -> str:
        return f'The refresh token not found'


@dataclass(eq=False)
class InvalidToken(ApplicationError):
    code: ClassVar[str] = "INVALID_ACCESS_TOKEN"

    @property
    def title(self) -> str:
        return "Token is invalid"


@dataclass(eq=False)
class ExpiredToken(ApplicationError):
    code: ClassVar[str] = "EXPIRED_ACCESS_TOKEN"

    @property
    def title(self) -> str:
        return "Token is expired"


@dataclass(eq=False)
class MismatchedAccessToken(ApplicationError):
    code: ClassVar[str] = "MISMATCHED_ACCESS_TOKEN"

    @property
    def title(self) -> str:
        return "Access token mismatch"


@dataclass(eq=False)
class InvalidCredentials(ApplicationError):
    code: ClassVar[str] = "INVALID_CREDENTIALS"

    @property
    def title(self) -> str:
        return "Invalid credentials"
