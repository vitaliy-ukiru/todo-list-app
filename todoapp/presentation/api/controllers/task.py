from typing import Annotated
from uuid import UUID

from didiator import Mediator
from fastapi import APIRouter, Depends

from todoapp.application.task.commands import CreateTask, DeleteTask, CompleteTask, PutTaskInList, \
    UpdateTask
from todoapp.application.task.queries import GetTaskById
from todoapp.application.task_list.exceptions import TaskListAccessError
from todoapp.domain.task.entities import Task
from todoapp.domain.user.entities import UserId
from todoapp.presentation.api.controllers.requests.task import CreateTaskRequest, UpdateTaskRequest
from todoapp.presentation.api.controllers.responses.base import OkResponse, OkStatus, OK_STATUS
from todoapp.presentation.api.doc import response_error_doc, DEFAULT_UUID
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import auth_user_by_token

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.post(
    "/",
    responses={
        403: response_error_doc(
            status=403,
            description="The user does not have access to the list",
            example=TaskListAccessError(DEFAULT_UUID)
        )
    }
)
async def create_task(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    body: CreateTaskRequest,
) -> OkResponse[Task]:
    task_id = await meditor.send(CreateTask(
        user_id=user_id,
        name=body.name,
        desc=body.desc,
        list_id=body.list_id
    ))

    task = await meditor.query(GetTaskById(
        task_id=task_id,
        user_id=user_id,
    ))

    return OkResponse(result=task)


@task_router.get(
    "/{task_id}"
)
async def get_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkResponse[Task]:
    task = await meditor.query(GetTaskById(
        task_id=task_id,
        user_id=user_id,
    ))

    return OkResponse(result=task)


@task_router.delete(
    "/{task_id}"
)
async def delete_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkStatus:
    await meditor.send(DeleteTask(
        task_id=task_id,
        user_id=user_id,
    ))

    return OK_STATUS


@task_router.post(
    "/{task_id}/complete",
)
async def complete_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkResponse[Task]:
    task = await meditor.send(CompleteTask(
        task_id=task_id,
        user_id=user_id,
    ))
    return OkResponse(result=task)


@task_router.put(
    "/{task_id}/to-list/{list_id}",
)
async def put_in_list(
    task_id: UUID,
    list_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkResponse[Task]:
    task = await meditor.send(PutTaskInList(
        task_id=task_id,
        list_id=list_id,
        user_id=user_id,
    ))
    return OkResponse(result=task)


@task_router.put(
    "/{task_id}"
)
async def update_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    body: UpdateTaskRequest,
) -> OkResponse[Task]:
    task = await meditor.send(UpdateTask(
        task_id=task_id,
        user_id=user_id,
        **body.model_dump(exclude_unset=True)
    ))
    return OkResponse(result=task)
