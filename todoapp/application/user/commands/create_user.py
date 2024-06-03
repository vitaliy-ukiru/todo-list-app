from dataclasses import dataclass
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr

from todoapp.application.common.command import Command, CommandHandler
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.user.interfaces import UserRepo
from todoapp.domain.user.entities import PasswordHasher, User


@dataclass
class CreateUser(Command[UUID]):
    email: str
    password: str


@dataclass
class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    user_repo: UserRepo
    uow: UnitOfWork
    hasher: PasswordHasher

    async def __call__(self, command: CreateUser) -> UUID:
        user = User.create(command.email, command.password, self.hasher)
        await self.user_repo.save_user(user)
        await self.uow.commit()

        return user.id
