from dataclasses import dataclass

from didiator import QueryMediator

from todoapp.application.auth.exceptions import InvalidCredentials
from todoapp.application.common.query import Query, QueryHandler
from todoapp.application.user.exceptions import EmailNotExistError
from todoapp.application.user.queries import GetUserByEmail
from todoapp.domain.user.entities import UserId, User, PasswordHasher
from todoapp.domain.user.exceptions import UserIsDeletedError


@dataclass
class AuthenticateByCredentials(Query[UserId]):
    email: str
    password: str


@dataclass
class AuthenticateByCredentialsHandler(QueryHandler[AuthenticateByCredentials, UserId]):
    mediator: QueryMediator
    hasher: PasswordHasher

    async def __call__(self, query: AuthenticateByCredentials) -> UserId:
        try:
            user = await self.mediator.query(GetUserByEmail(email=query.email))
        except (EmailNotExistError, UserIsDeletedError):
            raise InvalidCredentials()

        if not user.verify_password(self.hasher, query.password):
            raise InvalidCredentials()

        return user.id
