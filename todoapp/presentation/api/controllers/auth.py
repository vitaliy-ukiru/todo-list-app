from typing import Annotated

from di import ScopeState
from didiator import Mediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import APIRouter, Depends, Query, Response, Form
from pydantic import EmailStr
from starlette import status

from todoapp.application.auth.commands import ProduceTokens, RefreshTokens, DeactivateRefreshToken
from todoapp.application.auth.dto import Tokens
from todoapp.application.auth.exceptions import InvalidCredentials
from todoapp.application.auth.queries.auth_creds import AuthenticateByCredentials
from todoapp.common.settings import AuthConfig
from todoapp.infrastructure.di import DiScope
from todoapp.presentation.api.controllers.responses.base import OkResponse, OkStatus, OK_STATUS
from todoapp.presentation.api.doc import response_error_doc
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import bearer_header, REFRESH_TOKEN_COOKIE, refresh_cookie
from todoapp.presentation.api.providers.di import get_di_builder, get_di_state

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


async def _get_auth_config(
    di_builder: Annotated[DiBuilder, Depends(get_di_builder)],
    di_state: Annotated[ScopeState, Depends(get_di_state)],
) -> AuthConfig:
    cfg = await di_builder.execute(AuthConfig, scope=DiScope.REQUEST, state=di_state)
    return cfg


@auth_router.post(
    "/login",
    responses={
        status.HTTP_401_UNAUTHORIZED: response_error_doc(
            status=status.HTTP_401_UNAUTHORIZED,
            description="Invalid credentials",
            example=InvalidCredentials()
        )
    }
)
async def login_user(
    username: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    cfg: Annotated[AuthConfig, Depends(_get_auth_config)],
    response: Response,
    set_cookie: Annotated[bool, Query()] = True,
) -> OkResponse[Tokens]:
    user_id = await meditor.query(AuthenticateByCredentials(
        email=username,
        password=password,
    ))

    tokens = await meditor.send(ProduceTokens(
        user_id=user_id
    ))

    if set_cookie:
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE,
            value=tokens.refresh_token,
            max_age=int(cfg.refresh_token_expires.total_seconds()),
            httponly=True,
            path="/auth"
        )

    return OkResponse(result=tokens)


@auth_router.get("/refresh")
async def refresh_tokens(
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
    access_token: Annotated[str, Depends(bearer_header)],
    refresh_token: Annotated[str, Depends(refresh_cookie)],
    cfg: Annotated[AuthConfig, Depends(_get_auth_config)],
    response: Response,
) -> OkResponse[Tokens]:
    tokens = await mediator.send(RefreshTokens(
        access_token=access_token,
        refresh_token=refresh_token,
    ))

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=tokens.refresh_token,
        max_age=int(cfg.refresh_token_expires.total_seconds()),
        httponly=True,
        path="/auth"
    )

    return OkResponse(result=tokens)


@auth_router.post("/refresh/app")
async def refresh_tokens(
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
    body: Tokens,
) -> OkResponse[Tokens]:
    tokens = await mediator.send(RefreshTokens(
        access_token=body.access_token,
        refresh_token=body.refresh_token,
    ))

    return OkResponse(result=tokens)


@auth_router.get("/logout")
async def logout(
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
    refresh_token: Annotated[str, Depends(refresh_cookie)],
    response: Response,
) -> OkStatus:
    response.delete_cookie(REFRESH_TOKEN_COOKIE)
    await mediator.send(DeactivateRefreshToken(
        refresh_token=refresh_token,
    ))
    return OK_STATUS
