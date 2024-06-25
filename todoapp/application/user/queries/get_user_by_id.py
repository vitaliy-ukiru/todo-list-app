from dataclasses import dataclass
from uuid import UUID

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.user.interfaces import UserRepo
from todoapp.domain.user.entities import User, UserId
from todoapp.domain.user.exceptions import UserIsDeletedError


@dataclass
class GetUserById(Query[User]):
    user_id: UserId


@dataclass
class GetUserByIdHandler(QueryHandler[GetUserById, User]):
    repo: UserRepo

    async def __call__(self, query: GetUserById) -> User:
        user = await self.repo.get_user_by_id(query.user_id)
        return user
