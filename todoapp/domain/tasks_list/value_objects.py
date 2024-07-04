from typing import NewType, Annotated, Self
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from todoapp.domain.common.constants import Operation
from todoapp.domain.user.entities import UserId

ListId = NewType("ListId", UUID)


class SharingRule(BaseModel):
    update_task_allowed: bool
    manage_tasks_allowed: bool

    def __contains__(self, item: Operation) -> bool:
        if not isinstance(item, Operation):
            raise TypeError(f"Excepted type 'Operation', got {type(item)}")

        match item:
            case Operation.read:
                # if sharing rule presents it means that user can read
                # it minimum access.
                return True
            case Operation.update_task:
                return self.update_task_allowed
            case Operation.add_task_to_list | Operation.delete_task_from_list:
                return self.manage_tasks_allowed


class Sharing(BaseModel):
    public: Annotated[bool, Field(False)]
    collaborators: Annotated[dict[UserId, SharingRule], Field(default_factory=dict)]

    def can(self, user_id: UserId, op: Operation) -> bool:
        if self.public and op is Operation.read:
            return True

        rule = self.collaborators.get(user_id)
        if not rule:
            return False

        return op in rule
