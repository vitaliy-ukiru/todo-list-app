from typing import Annotated

from pydantic import Field

from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.tasks_list.value_objects import ListId
from todoapp.domain.user.entities import User


class TaskList(BaseEntity[ListId]):
    name: Annotated[str, Field(min_length=3, max_length=500)]
    user: User
