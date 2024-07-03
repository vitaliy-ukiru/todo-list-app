from typing import Annotated
from uuid import UUID

from didiator import Mediator
from fastapi import APIRouter, Depends

from todoapp.application.task_list.commands import CreateTaskList, DeleteTaskList, AddTaskToList
from todoapp.application.task_list.queries import GetListById
from todoapp.domain.tasks_list.entities import TaskList
from todoapp.domain.user.entities import UserId
from todoapp.presentation.api.controllers.requests.task_list import CreateTaskListRequest
from todoapp.presentation.api.controllers.responses.base import OkResponse, OkStatus, OK_STATUS
from todoapp.presentation.api.controllers.responses.task_list import TaskListIdResponse
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import auth_user_by_token

task_list_router = APIRouter(prefix="/task-list", tags=["task-list"])


@task_list_router.post("/")
async def create_task_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    body: CreateTaskListRequest,
) -> OkResponse[TaskListIdResponse]:
    task_list_id = await meditor.send(CreateTaskList(
        name=body.name,
        user_id=user_id,
    ))

    return OkResponse(result=TaskListIdResponse(list_id=task_list_id))


@task_list_router.get("/{list_id}")
async def get_task_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    list_id: UUID,
) -> OkResponse[TaskList]:
    task_list = await meditor.query(GetListById(list_id=list_id, user_id=user_id))
    return OkResponse(result=task_list)


@task_list_router.delete("/{list_id}")
async def delete_task_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    list_id: UUID,
) -> OkStatus:
    await meditor.send(DeleteTaskList(list_id=list_id, user_id=user_id))
    return OK_STATUS


@task_list_router.put("/{list_id}/add/{task_id}")
async def add_task_to_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    list_id: UUID,
    task_id: UUID,
) -> OkResponse[TaskList]:
    task_list = await meditor.send(AddTaskToList(
        list_id=list_id,
        task_id=task_id,
        user_id=user_id,
    ))
    return OkResponse(result=task_list)
