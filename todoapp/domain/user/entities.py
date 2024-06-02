import abc
from datetime import datetime
from typing import NewType, Annotated, Protocol, Self
from uuid import UUID

from pydantic import EmailStr, SecretStr, Field
from uuid6 import uuid7

from todoapp.domain.common.entities import BaseEntity

UserId = NewType("UserId", UUID)


class PasswordHasher(Protocol):
    @abc.abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, hashed_password: str, password: str) -> bool:
        raise NotImplementedError


class User(BaseEntity[UserId]):
    email: EmailStr
    password: Annotated[SecretStr, Field(exclude=True)]

    @classmethod
    def create(
        cls,
        email: str,
        password: str,
        hasher: PasswordHasher
    ) -> Self:
        creation_time = datetime.utcnow()
        user_id = UserId(uuid7())
        return cls(
            id=user_id,
            email=email,
            password=hasher.hash(password),
            created_at=creation_time,
        )

    def verify_password(self, hasher: PasswordHasher, password: str) -> bool:
        return hasher.verify(self.password.get_secret_value(), password)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def delete(self):
        self.deleted_at = datetime.utcnow()
