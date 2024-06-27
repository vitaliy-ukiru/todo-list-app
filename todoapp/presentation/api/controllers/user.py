from dataclasses import dataclass
from typing import Annotated, Literal
from uuid import UUID

from didiator import Mediator
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from starlette import status

from todoapp.application.user.commands import CreateUser
from todoapp.application.user.dto import User
from todoapp.domain.user.exceptions import EmailAlreadyExistsError
from todoapp.presentation.api.controllers.responses.base import OkResponse
from todoapp.presentation.api.doc import response_error_doc
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import get_current_user

user_router = APIRouter(prefix="/user", tags=["user"])


@dataclass(frozen=True)
class SignUpUserResponse:
    user_id: UUID


@user_router.post(
    "/sign-up",
    responses={
        status.HTTP_409_CONFLICT: response_error_doc(
            status=status.HTTP_409_CONFLICT,
            description="User with same email already exists",
            example=EmailAlreadyExistsError("{email}"),
        )
    }
)
async def signup_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    meditor: Annotated[Mediator, Depends(Stub(Mediator))]
) -> OkResponse[SignUpUserResponse]:
    user_id = await meditor.send(CreateUser(
        email=email,
        password=password,
    ))
    return OkResponse(result=SignUpUserResponse(user_id))


# this endpoint only for test auth
@user_router.get(path="/email")
async def get_email(
    user: Annotated[User, Depends(get_current_user)],
) -> OkResponse[str]:
    return OkResponse(result=user.email)
