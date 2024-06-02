from typing import NoReturn

from sqlalchemy.exc import DBAPIError, IntegrityError

from todoapp.application.common.exceptions import RepoError
from todoapp.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError
from todoapp.application.user.interfaces.repo import UserRepo
from todoapp.domain.user import entities
from todoapp.domain.user.exceptions import EmailAlreadyExistsError
from todoapp.infra.db.repo.exception_mapper import exception_mapper
from todoapp.infra.db.models import User
from todoapp.infra.db.repo.base import SQLAlchemyRepo


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def acquire_user_by_id(self, user_id: entities.UserId) -> entities.User:
        user: User | None = await self._session.get(
            User,
            user_id,
            with_for_update=True
        )
        if user is None:
            raise UserIdNotExistError(user_id)

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
        id=user.id,
        email=user.email,
        password=user.password_hash,
        created_at=user.created_at,
        deleted_at=user.deleted_at,
    )


def convert_entity_to_db_model(user: entities.User) -> User:
    return User(
        id=user.id,
        email=user.email,
        password_hash=user.password.get_secret_value(),
        created_at=user.created_at,
        deleted_at=user.deleted_at,
    )
