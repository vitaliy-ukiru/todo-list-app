from typing import NewType, Annotated, Self
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from todoapp.domain.common.constants import Operation
from todoapp.domain.user.entities import UserId

ListId = NewType("ListId", UUID)


class SharingRule(BaseModel):
    read_allowed: bool
    update_task_allowed: bool
    manage_tasks_allowed: bool

    @model_validator(mode="after")
    def validate_read_access(self) -> Self:
        changes_allowed = self.update_task_allowed or self.read_allowed
        if not self.read_allowed and changes_allowed:
            raise ValueError("The rule allows change state of an object, but does not allow to read")

        return self

    def __contains__(self, item: Operation) -> bool:
        if not isinstance(item, Operation):
            raise TypeError(f"Excepted type 'Operation', got {type(item)}")

        match item:
            case Operation.read:
                return self.read_allowed
            case Operation.update_task:
                return self.update_task_allowed
            case Operation.add_task_to_list, Operation.delete_task_from_list:
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
