from todoapp.application.common.pagination import Pagination, SortOrder


def get_pagination(
    offset: int | None = None,
    limit: int | None = None,
    order: SortOrder = SortOrder.ASC
) -> Pagination:
    return Pagination(offset=offset, limit=limit, order=order)
