from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel

from todoapp.domain.common.value_objects import DateTimeNull

IdT = TypeVar('IdT')


class BaseEntity(BaseModel[IdT]):
    id: IdT
    created_at: datetime
    deleted_at: DateTimeNull = None
