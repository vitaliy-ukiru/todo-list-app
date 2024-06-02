from enum import Enum
from typing import Generic, TypeVar, Self

from todoapp.application.common.dto import DTO

Item = TypeVar("Item")


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class Pagination(DTO):
    offset: int | None = None
    limit: int | None = None
    order: SortOrder = SortOrder.ASC


class PaginationResult(DTO):
    offset: int | None
    limit: int | None
    total: int
    order: SortOrder

    @classmethod
    def from_pagination(cls, pagination: Pagination, total: int) -> Self:
        return cls(
            offset=pagination.offset,
            limit=pagination.limit,
            order=pagination.order,
            total=total,
        )


class PaginatedItemsDTO(DTO, Generic[Item]):
    data: list[Item]
    pagination: PaginationResult
