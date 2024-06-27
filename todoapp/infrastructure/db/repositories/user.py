from typing import NoReturn

from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError

from todoapp.application.common.exceptions import RepoError
from todoapp.application.user import dto
from todoapp.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError, \
    UserEmailNotExistError
from todoapp.application.user.interfaces import UserRepo
from todoapp.domain.user import entities
from todoapp.domain.user.entities import UserId
from todoapp.domain.user.exceptions import EmailAlreadyExistsError, UserIsDeletedError
from todoapp.infrastructure.db.models import User
from .base import SQLAlchemyRepo
from .exception_mapper import exception_mapper


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def get_user_by_id(self, user_id: entities.UserId) -> dto.User:
        user: User | None = await self._session.get(
            User,
            user_id,
            with_for_update=True
        )
        if user is None:
            raise UserIdNotExistError(user_id)

        return convert_model_to_entity(user)

    @exception_mapper
    async def acquire_user_by_email(self, email: str) -> entities.User:
        user: User | None = await self._session.scalar(
            select(User).where(User.email == email)
        )
        if user is None:
            raise UserEmailNotExistError(email)

        return convert_model_to_entity(user)

    @exception_mapper
    async def save_user(self, user: entities.User) -> None:
        model = convert_entity_to_db_model(user)
        self._session.add(model)
        try:
            await self._session.flush((model,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def update_user(self, user: entities.User) -> None:
        model = convert_entity_to_db_model(user)
        try:
            await self._session.merge(model)
        except IntegrityError as err:
            self._parse_error(err, user)

    @staticmethod
    def _parse_error(err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "users_pkey":
                raise UserIdAlreadyExistsError(user.id) from err
            case "ix_users_email":
                raise EmailAlreadyExistsError(str(user.email)) from err
            case _:
                raise RepoError from err


def convert_model_to_entity(user: User) -> entities.User:
    return entities.User(
        id=UserId(user.id),
        email=user.email,
        password=SecretStr(user.password_hash),
        created_at=user.created_at,
        deleted_at=user.deleted_at,
    )

def convert_model_to_dto(user: User) -> dto.User:
    user_id = UserId(user.id)
    if user.deleted_at is not None:
        raise UserIsDeletedError(user_id)

    return dto.User(
        id=user_id,
        email=user.email
    )


def convert_entity_to_db_model(user: entities.User) -> User:
    return User(
        id=user.id,
        email=user.email,
        password_hash=user.password.get_secret_value(),
        created_at=user.created_at,
        deleted_at=user.deleted_at,
    )
