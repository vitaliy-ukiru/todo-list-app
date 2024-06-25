from dataclasses import dataclass

from todoapp.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class RefreshTokenNotFound(ApplicationError):
    status = 401

    refresh_token: str

    @property
    def title(self) -> str:
        return f'The refresh token {self.refresh_token!r} not found'


@dataclass(eq=False)
class InvalidToken(ApplicationError):
    status = 401

    @property
    def title(self) -> str:
        return "Token is invalid"


@dataclass(eq=False)
class ExpiredToken(ApplicationError):
    status = 401

    @property
    def title(self) -> str:
        return "Token is expired"


@dataclass(eq=False)
class MismatchAccessToken(ApplicationError):
    status = 401

    @property
    def title(self) -> str:
        return "Access token mismatch"


@dataclass(eq=False)
class InvalidCredentials(ApplicationError):
    status = 401

    @property
    def title(self) -> str:
        return "Invalid credentials"
