from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from todoapp.application.common.dto import DTO

Item = TypeVar("Item")


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True)
class Pagination:
    offset: int | None = None
    limit: int | None = None
    order: SortOrder = SortOrder.ASC


@dataclass(frozen=True)
class PaginationResult(DTO):
    offset: int | None
    limit: int | None
    total: int
    order: SortOrder

    @classmethod
    def from_pagination(cls, pagination: Pagination, total: int) -> "PaginationResult":
        offset = pagination.offset
        limit = pagination.limit
        return cls(offset=offset, limit=limit, order=pagination.order, total=total)


@dataclass(frozen=True)
class PaginatedItemsDTO(DTO, Generic[Item]):
    data: list[Item]
    pagination: PaginationResult
