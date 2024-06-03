from datetime import datetime
from typing import TypeVar, Generic, Self
from uuid import UUID

from pydantic import BaseModel

IdT = TypeVar('IdT', bound=UUID)


class BaseEntity(BaseModel, Generic[IdT]):
    id: IdT
    created_at: datetime

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id
