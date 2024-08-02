from datetime import datetime
from typing import Annotated, Self

from pydantic import Field
from uuid6 import uuid7

from todoapp.domain.common.constants import Operation
from todoapp.domain.common.entities import BaseEntity
from todoapp.domain.task_list.exceptions import TaskListVisibilityNotModified, SharingRuleNotExistsError
from todoapp.domain.task_list.value_objects import ListId, Sharing, SharingRule
from todoapp.domain.user.entities import UserId

MAX_TASK_LIST_NAME_LENGTH = 500
MIN_TASK_LIST_NAME_LENGTH = 3


class TaskList(BaseEntity[ListId]):
    name: Annotated[
        str,
        Field(min_length=MIN_TASK_LIST_NAME_LENGTH, max_length=MAX_TASK_LIST_NAME_LENGTH)
    ]
    user_id: UserId
    sharing: Annotated[Sharing, Field(default_factory=Sharing)]

    def is_have_access(self, user_id: UserId, op: Operation) -> bool:
        if self.user_id == user_id:
            return True

        return self.sharing.can(user_id, op)

    @classmethod
    def create(
        cls,
        name: str,
        user_id: UserId,
        public: bool = False,
    ) -> Self:
        created_at = datetime.utcnow()
        list_id = ListId(uuid7())
        return cls(
            id=list_id,
            name=name,
            user_id=user_id,
            created_at=created_at,
            sharing=Sharing(public=public)
        )

    def change_visibility(self, public: bool):
        if self.sharing.public == public:
            raise TaskListVisibilityNotModified()

        self.sharing.public = public

    def set_sharing_rule(self, collaborator: UserId, rule: SharingRule):
        self.sharing.collaborators[collaborator] = rule

    def delete_collaborator(self, collaborator: UserId):
        if collaborator not in self.sharing.collaborators:
            raise SharingRuleNotExistsError(
                list_id=self.id,
                user_id=collaborator,
            )

        del self.sharing.collaborators[collaborator]
