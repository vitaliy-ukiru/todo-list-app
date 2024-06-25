from datetime import timedelta

from redis.asyncio.client import Redis

from todoapp.application.auth.exceptions import RefreshTokenNotFound
from todoapp.application.auth.interfaces.repository import TokensRepo, TokenKey


class TokensRepoImpl(TokensRepo):
    def __init__(
        self,
        client: Redis,
        token_ttl: timedelta | None = None
    ):
        self._client = client
        self._token_ttl = token_ttl

    async def save_token(self, token_key: TokenKey, access_token_id: str):
        key = self._build_key(token_key)
        await self._client.set(key, access_token_id, ex=self._token_ttl)

    async def get_token(self, token_key: TokenKey) -> str:
        key = self._build_key(token_key)
        access_token_id = await self._client.get(key)
        if access_token_id is None:
            raise RefreshTokenNotFound(token_key.refresh_token_id)

        if isinstance(access_token_id, bytes):
            access_token_id = access_token_id.decode("utf-8")

        return access_token_id

    async def delete_token(self, key: TokenKey):
        count_of_delete_items = await self._client.delete(self._build_key(key))
        if count_of_delete_items == 0:
            raise RefreshTokenNotFound(key.refresh_token_id)

    @staticmethod
    def _build_key(token: TokenKey) -> str:
        # now one user - one refresh token
        # in future it will be updated
        # TODO: add support to multiply session with managing
        return f'auth:refresh:{token.user_id}'
