from datetime import datetime
from typing import TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel

IdT = TypeVar('IdT', bound=UUID)


class BaseEntity(BaseModel, Generic[IdT]):
    id: IdT
    created_at: datetime
