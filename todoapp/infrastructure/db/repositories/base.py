from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from todoapp.application.common.pagination import Pagination
from todoapp.application.common.query import Query


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def apply_pagination(query: Select, pagination: Pagination) -> Select:
        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)
        return query
