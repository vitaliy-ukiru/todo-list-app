from dataclasses import dataclass
from typing import Generic, TypeVar, Annotated

from pydantic import BaseModel, Field

from todoapp.domain.common.exceptions import AppError

TResult = TypeVar("TResult")
TError = TypeVar("TError")


class Response(BaseModel):
    ok: bool


class OkResponse(Response, Generic[TResult]):
    ok: bool = True
    result: TResult | None = None


class ErrorData(BaseModel, Generic[TError]):
    code: str = "UNKNOWN_ERROR"
    title: str = "Unknown error occurred"
    status: int = 500
    data: TError | None = None

    @classmethod
    def from_error(cls, err: AppError, status_code: int):
        return cls(
            code=err.code,
            title=err.title,
            data=err,
            status=status_code,
        )


class ErrorResponse(Response, Generic[TError]):
    ok: Annotated[bool, Field(default=False, init=False)]
    error: Annotated[ErrorData[TError], Field(default_factory=ErrorData)]


class OkStatus(Response):
    ok: bool = True


OK_STATUS = OkStatus()
