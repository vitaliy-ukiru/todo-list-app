from typing import Annotated

from didiator import QueryMediator
from fastapi import Depends
from fastapi.security import HTTPBearer, APIKeyCookie, HTTPAuthorizationCredentials

from todoapp.application.auth.exceptions import AccessTokenRequired, RefreshTokenRequired
from todoapp.application.auth.queries.auth_token import AuthenticateByToken
from todoapp.application.user import dto
from todoapp.application.user.queries import GetUserById
from todoapp.domain.user.entities import UserId
from todoapp.presentation.api.providers import Stub

REFRESH_TOKEN_COOKIE = "refresh_token"

_bearer_header = HTTPBearer(auto_error=False)


def bearer_header(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_header)]
) -> str:
    if not creds:
        raise AccessTokenRequired()

    return creds.credentials


optional_refresh_cookie = APIKeyCookie(
    name=REFRESH_TOKEN_COOKIE,
    auto_error=False,
)


def refresh_cookie(token: Annotated[str | None, Depends(optional_refresh_cookie)]) -> str:
    if not token:
        raise RefreshTokenRequired()

    return token


async def auth_user_by_token(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    access_token: Annotated[str, Depends(bearer_header)],
) -> UserId:
    user_id = await mediator.query(AuthenticateByToken(
        access_token=access_token,
    ))
    return user_id


async def get_current_user(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> dto.User:
    user = await mediator.query(GetUserById(user_id))
    return user
