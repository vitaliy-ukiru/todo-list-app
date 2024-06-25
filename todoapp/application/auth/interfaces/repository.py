from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from todoapp.domain.user.entities import UserId


@dataclass
class TokenKey:
    user_id: UserId
    refresh_token_id: str


class TokensRepo(Protocol):
    @abstractmethod
    async def save_token(
        self,
        key: TokenKey,
        access_token_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_token(
        self,
        token_key: TokenKey,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def delete_token(self, token_key: TokenKey):
        raise NotImplementedError
