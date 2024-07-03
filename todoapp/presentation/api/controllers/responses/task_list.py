from uuid import UUID

from pydantic import BaseModel


class TaskListIdResponse(BaseModel):
    list_id: UUID