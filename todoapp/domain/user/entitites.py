from typing import NewType, Annotated

from pydantic import UUID4, EmailStr, SecretStr, Field

from todoapp.domain.common.entities import BaseEntity

UserId = NewType("UserId", UUID4)


class User(BaseEntity[UserId]):
    email: EmailStr
    password: Annotated[SecretStr, Field(min_length=8, exclude=True)]
