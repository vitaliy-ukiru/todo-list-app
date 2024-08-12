from typing import Annotated

from pydantic import BaseModel, Field

from todoapp.domain.task_list.entities import MIN_TASK_LIST_NAME_LENGTH, MAX_TASK_LIST_NAME_LENGTH


class CreateTaskListRequest(BaseModel):
    name: Annotated[
        str,
        Field(min_length=MIN_TASK_LIST_NAME_LENGTH, max_length=MAX_TASK_LIST_NAME_LENGTH)
    ]


class ShareRequest(BaseModel):
    allow_update_tasks: bool = False
    allow_manage_tasks: bool = False
