from dataclasses import dataclass

from todoapp.application.auth.jwt import JWTAuthenticator
from todoapp.application.common.query import Query, QueryHandler
from todoapp.domain.user.entities import UserId


@dataclass
class AuthenticateByToken(Query[UserId]):
    access_token: str


@dataclass
class AuthenticateByTokenHandler(QueryHandler[AuthenticateByToken, UserId]):
    auth: JWTAuthenticator

    async def __call__(self, query: AuthenticateByToken) -> UserId:
        access_token = self.auth.decode_access_token(query.access_token)
        return access_token.user_id
