from dataclasses import dataclass

from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.user.interfaces import UserRepo
from todoapp.domain.user.entities import User
from todoapp.domain.user.exceptions import UserIsDeletedError


@dataclass
class GetUserByEmail(Query[User]):
    email: str


@dataclass
class GetUserByEmailHandler(QueryHandler[GetUserByEmail, User]):
    repo: UserRepo

    async def __call__(self, query: GetUserByEmail) -> User:
        user = await self.repo.acquire_user_by_email(query.email)
        if user.is_deleted:
            raise UserIsDeletedError(user.id)

        return user
