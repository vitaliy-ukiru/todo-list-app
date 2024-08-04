from typing import Annotated, Literal, cast
from uuid import UUID

from didiator import Mediator
from fastapi import APIRouter, Depends

from todoapp.application.common.pagination import Pagination
from todoapp.application.task import dto
from todoapp.application.task.commands import (CreateTask, DeleteTask, CompleteTask, PutTaskInList,
                                               UpdateTask)
from todoapp.application.task.exceptions import TaskAccessError
from todoapp.application.task.queries import GetTaskById, FindTasks
from todoapp.application.task_list.exceptions import TaskListAccessError, TaskListNotExistsError
from todoapp.domain.common.constants import Empty
from todoapp.domain.user.entities import UserId
from todoapp.presentation.api.controllers.requests.task import CreateTaskRequest, UpdateTaskRequest
from todoapp.presentation.api.controllers.responses.base import OkResponse, OkStatus, OK_STATUS
from todoapp.presentation.api.doc import response_error_doc, DEFAULT_UUID, RESPONSE_NOT_AUTHENTICATED
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import auth_user_by_token
from todoapp.presentation.api.providers.pagination import get_pagination

task_router = APIRouter(
    prefix="/task",
    tags=["task"],
    responses={
        401: RESPONSE_NOT_AUTHENTICATED,
    }
)

_BASE_RESPONSES = {
    403: response_error_doc(
        status=403,
        description="The user does not access to the task",
        example=TaskAccessError(DEFAULT_UUID)
    ),
    404: response_error_doc(
        status=401,
        description="The task is not exists",
        example=TaskListNotExistsError(DEFAULT_UUID)
    )
}


@task_router.post(
    "/",
    responses={
        403: response_error_doc(
            status=403,
            description="The user does not have access to the task list",
            example=TaskListAccessError(DEFAULT_UUID)
        )
    }
)
async def create_task(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    body: CreateTaskRequest,
) -> OkResponse[dto.Task]:
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
    "/{task_id}",
    responses=_BASE_RESPONSES
)
async def get_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkResponse[dto.Task]:
    task = await meditor.query(GetTaskById(
        task_id=task_id,
        user_id=user_id,
    ))

    return OkResponse(result=task)


@task_router.delete(
    "/{task_id}",
    responses=_BASE_RESPONSES
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
    responses=_BASE_RESPONSES
)
async def complete_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkResponse[dto.Task]:
    task = await meditor.send(CompleteTask(
        task_id=task_id,
        user_id=user_id,
    ))
    return OkResponse(result=task)


@task_router.patch(
    "/{task_id}/to/{list_id}",
    responses=_BASE_RESPONSES
)
async def put_in_list(
    task_id: UUID,
    list_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
) -> OkResponse[dto.Task]:
    task = await meditor.send(PutTaskInList(
        task_id=task_id,
        list_id=list_id,
        user_id=user_id,
    ))
    return OkResponse(result=task)


@task_router.patch(
    "/{task_id}",
    responses=_BASE_RESPONSES
)
async def update_task(
    task_id: UUID,
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    body: UpdateTaskRequest,
) -> OkResponse[dto.Task]:
    task = await meditor.send(UpdateTask(
        task_id=task_id,
        user_id=user_id,
        **body.model_dump(exclude_unset=True)
    ))
    return OkResponse(result=task)


@task_router.get("/")
async def find_tasks(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],

    pagination: Annotated[Pagination, Depends(get_pagination)],
    name: str | None = None,
    desc: str | None = None,
    completed: bool | None = None,
    list_id: UUID | Literal["null"] | None = None,
    shared: bool | None = None
) -> OkResponse[dto.TasksDTO]:
    if list_id is None:
        list_id = Empty.UNSET
    elif list_id == "null":
        list_id = None

    filters = dto.FindTasksFilters(
        user_id=user_id,
        name=name,
        desc=desc,
        completed=completed if completed is not None else Empty.UNSET,
        list_id=cast(UUID | None | Empty, list_id),
        shared_access=shared if shared is not None else Empty.UNSET
    )

    tasks = await meditor.query(FindTasks(
        filters=filters,
        pagination=pagination,
    ))
    return OkResponse(result=tasks)
