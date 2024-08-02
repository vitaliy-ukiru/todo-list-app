from typing import NewType, Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from todoapp.domain.common.constants import Operation
from todoapp.domain.user.entities import UserId

ListId = NewType("ListId", UUID)


class SharingRule(BaseModel):
    update_task_allowed: bool
    manage_tasks_allowed: bool

    def __contains__(self, item: Operation) -> bool:
        if not isinstance(item, Operation):
            raise TypeError(f"Excepted type 'Operation', got {type(item)}")

        return self.is_operation_allowed(item)

    def is_operation_allowed(self, op: Operation) -> bool:
        match op:
            case Operation.read:
                # if sharing rule presents it means that user can read
                # it minimum access.
                return True
            case Operation.update_task:
                return self.update_task_allowed
            case Operation.add_task_to_list | Operation.delete_task_from_list:
                return self.manage_tasks_allowed

        # Other operations available only for resource owner
        # May be this will change later
        return False


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
