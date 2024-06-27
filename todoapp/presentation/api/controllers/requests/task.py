from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from todoapp.domain.task.constants import MIN_NAME_LENGTH, MAX_NAME_LENGTH, MAX_DESC_LENGTH


class CreateTaskRequest(BaseModel):
    name: Annotated[str, Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)]
    desc: Annotated[str | None, Field(default=None, max_length=MAX_DESC_LENGTH)]
    list_id: Annotated[UUID | None, Field(default=None)]


class UpdateTaskRequest(BaseModel):
    name: Annotated[
        str | None,
        Field(default=None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    ]
    desc: Annotated[
        str | None,
        Field(default=None, max_length=MAX_DESC_LENGTH)
    ]
