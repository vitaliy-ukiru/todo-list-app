from pydantic import EmailStr

from todoapp.application.common.dto import DTO
from todoapp.domain.user.entities import UserId


class User(DTO):
    id: UserId
    email: EmailStr
