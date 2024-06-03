from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from todoapp.application.user.commands import CreateUser
from todoapp.presentation.api.providers import Stub

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/")
async def create_user(
    command: CreateUser,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))]
):
    user_id = await meditor.send(command)
    return {"user_id": user_id}
