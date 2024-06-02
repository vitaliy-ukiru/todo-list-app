import abc
from typing import Protocol

from todoapp.domain.user.entities import User, UserId


class UserRepo(Protocol):
    @abc.abstractmethod
    async def acquire_user_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError
