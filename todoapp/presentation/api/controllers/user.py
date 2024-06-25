from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr, Field

from todoapp.application.user.commands import CreateUser
from todoapp.application.user.dto import User
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import get_current_user

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/sign-up")
async def create_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    meditor: Annotated[Mediator, Depends(Stub(Mediator))]
):
    user_id = await meditor.send(CreateUser(
        email=email,
        password=password,
    ))
    return {"user_id": user_id}


# this endpoint only for test auth
@user_router.get(path="/email")
async def get_email(
    user: Annotated[User, Depends(get_current_user)],
):
    return {"email": user.email}
