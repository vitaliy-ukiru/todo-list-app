import abc
from typing import Protocol

from todoapp.application.user import dto
from todoapp.domain.user.entities import User, UserId


class UserRepo(Protocol):
    @abc.abstractmethod
    async def get_user_by_id(self, user_id: UserId) -> dto.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def acquire_user_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError
