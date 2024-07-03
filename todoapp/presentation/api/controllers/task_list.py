from typing import Annotated
from uuid import UUID

from didiator import Mediator
from fastapi import APIRouter, Depends

from todoapp.application.common.pagination import Pagination
from todoapp.application.task_list import dto
from todoapp.application.task_list.commands import CreateTaskList, DeleteTaskList, AddTaskToList
from todoapp.application.task_list.dto import TaskListsDTO, FindTaskListsFilters
from todoapp.application.task_list.exceptions import TaskListAccessError, TaskListNotExistsError
from todoapp.application.task_list.queries import GetListById
from todoapp.application.task_list.queries.find_tasks_lists import FindTaskLists
from todoapp.domain.tasks_list.exception import TaskAlreadyInList
from todoapp.domain.user.entities import UserId
from todoapp.presentation.api.controllers.requests.task_list import CreateTaskListRequest
from todoapp.presentation.api.controllers.responses.base import OkResponse, OkStatus, OK_STATUS
from todoapp.presentation.api.controllers.responses.task_list import TaskListIdResponse
from todoapp.presentation.api.doc import RESPONSE_NOT_AUTHENTICATED, response_error_doc, DEFAULT_UUID
from todoapp.presentation.api.providers import Stub
from todoapp.presentation.api.providers.auth import auth_user_by_token
from todoapp.presentation.api.providers.pagination import get_pagination

task_list_router = APIRouter(
    prefix="/task-list",
    tags=["task-list"],
    responses={
        401: RESPONSE_NOT_AUTHENTICATED,
    }
)

_BASE_RESPONSES = {
    403: response_error_doc(
        status=403,
        description="The user does not have access to the task list",
        example=TaskListAccessError(DEFAULT_UUID)
    ),
    404: response_error_doc(
        status=401,
        description="The task list is not exists",
        example=TaskListNotExistsError(DEFAULT_UUID)
    )
}


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


@task_list_router.get("/{list_id}", responses=_BASE_RESPONSES)
async def get_task_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    list_id: UUID,
) -> OkResponse[dto.TaskList]:
    task_list = await meditor.query(GetListById(list_id=list_id, user_id=user_id))
    return OkResponse(result=task_list)


@task_list_router.delete("/{list_id}", responses=_BASE_RESPONSES)
async def delete_task_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    list_id: UUID,
) -> OkStatus:
    await meditor.send(DeleteTaskList(list_id=list_id, user_id=user_id))
    return OK_STATUS


@task_list_router.put(
    "/{list_id}/add/{task_id}",
    responses=_BASE_RESPONSES | {
        409: response_error_doc(
            status=409,
            description="Task already in list",
            example=TaskAlreadyInList(DEFAULT_UUID, DEFAULT_UUID)
        )
    }
)
async def add_task_to_list(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],
    list_id: UUID,
    task_id: UUID,
) -> OkResponse[dto.TaskList]:
    task_list = await meditor.send(AddTaskToList(
        list_id=list_id,
        task_id=task_id,
        user_id=user_id,
    ))
    return OkResponse(result=task_list)


@task_list_router.get("/")
async def find_tasks(
    meditor: Annotated[Mediator, Depends(Stub(Mediator))],
    user_id: Annotated[UserId, Depends(auth_user_by_token)],

    pagination: Annotated[Pagination, Depends(get_pagination)],
    name: str | None = None,
) -> OkResponse[TaskListsDTO]:
    filters = FindTaskListsFilters(
        user_id=user_id,
        name=name,
    )

    tasks = await meditor.query(FindTaskLists(
        filters=filters,
        pagination=pagination,
    ))
    return OkResponse(result=tasks)
