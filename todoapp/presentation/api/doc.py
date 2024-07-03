from typing import TypeVar
from uuid import UUID

from todoapp.application.auth.exceptions import AccessTokenRequired
from todoapp.domain.common.exceptions import AppError
from todoapp.presentation.api.controllers.responses.base import ErrorResponse, ErrorData

T = TypeVar('T', bound=AppError)

DEFAULT_UUID = UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")


def response_error_doc(
    status: int,
    description: str,
    example: T,
):
    return {
        "model": ErrorResponse[type(example)],
        "description": description,
        "content": {
            "application/json": {
                "example": ErrorResponse(
                    error=ErrorData.from_error(example, status)
                )
            }
        }
    }


RESPONSE_NOT_AUTHENTICATED = response_error_doc(
    status=401,
    description="User not authenticated",
    example=AccessTokenRequired()
)
