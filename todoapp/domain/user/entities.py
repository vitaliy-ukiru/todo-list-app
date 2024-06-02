from typing import NewType, Annotated
from uuid import UUID

from pydantic import EmailStr, SecretStr, Field

from todoapp.domain.common.entities import BaseEntity

UserId = NewType("UserId", UUID)


class User(BaseEntity[UserId]):
    email: EmailStr
    password: Annotated[SecretStr, Field(min_length=8, exclude=True)]
