from dataclasses import dataclass
from uuid import UUID

from didiator import Mediator

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.user.interfaces import UserRepo
from todoapp.domain.user.entities import PasswordHasher, User


@dataclass
class CreateUser(Command[UUID]):
    email: str
    password: str


class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: Mediator,
        hasher: PasswordHasher,
    ) -> None:
        self._hasher = hasher
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> UUID:
        user = User.create(command.email, command.password, self._hasher)
        await self._user_repo.save_user(user)
        await self._uow.commit()

        return user.id
