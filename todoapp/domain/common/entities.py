from datetime import datetime
from typing import TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel

from todoapp.domain.common.value_objects import DateTimeNull

IdT = TypeVar('IdT', bound=UUID)


class BaseEntity(BaseModel, Generic[IdT]):
    id: IdT
    created_at: datetime
    deleted_at: DateTimeNull = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

