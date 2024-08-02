import functools
import logging
from typing import Callable, Awaitable

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from todoapp.application.auth.exceptions import (
    RefreshTokenNotFound,
    InvalidToken,
    ExpiredToken,
    MismatchedAccessToken,
    InvalidCredentials,
    AccessTokenRequired, RefreshTokenRequired
)
from todoapp.application.task.exceptions import (
    TaskAlreadyExistsError,
    TaskNotExistsError,
    TaskAccessError,
)
from todoapp.application.task_list.exceptions import (
    TaskListAccessError,
    TaskListNotExistsError,
    TaskListAlreadyExistsError
)
from todoapp.application.user.exceptions import (
    UserIdAlreadyExistsError,
    UserIdNotExistError,
    UserEmailNotExistError,
)
from todoapp.domain.common.exceptions import AppError
from todoapp.domain.task.exceptions import (
    TaskDescOutOfRange,
    TaskNameOutOfRange,
)
from todoapp.domain.tasks_list.exceptions import (
    TaskAlreadyInList,
    SharingRuleNotExistsError,
    TaskListVisibilityNotModified,
)
from todoapp.domain.user.exceptions import (
    UserIsDeletedError,
    EmailAlreadyExistsError
)
from todoapp.presentation.api.controllers.responses.base import ErrorResponse, ErrorData

logger = logging.getLogger(__name__)

_USER_EXC = {
    # application
    UserIdNotExistError: status.HTTP_404_NOT_FOUND,
    UserEmailNotExistError: status.HTTP_404_NOT_FOUND,
    UserIdAlreadyExistsError: status.HTTP_409_CONFLICT,

    # domain
    UserIsDeletedError: status.HTTP_409_CONFLICT,
    EmailAlreadyExistsError: status.HTTP_409_CONFLICT,
}

_TASK_EXC = {
    TaskAlreadyExistsError: status.HTTP_409_CONFLICT,
    TaskNotExistsError: status.HTTP_404_NOT_FOUND,
    TaskAccessError: status.HTTP_403_FORBIDDEN,

    # domain
    TaskDescOutOfRange: status.HTTP_400_BAD_REQUEST,
    TaskNameOutOfRange: status.HTTP_400_BAD_REQUEST,
}

_TASK_LIST_EXC = {
    TaskListAccessError: status.HTTP_403_FORBIDDEN,
    TaskListNotExistsError: status.HTTP_404_NOT_FOUND,
    TaskListAlreadyExistsError: status.HTTP_409_CONFLICT,
    SharingRuleNotExistsError: status.HTTP_404_NOT_FOUND,
    TaskListVisibilityNotModified: status.HTTP_409_CONFLICT,

    # domain
    TaskAlreadyInList: status.HTTP_409_CONFLICT,
}

_AUTH_EXC = {
    RefreshTokenNotFound: status.HTTP_401_UNAUTHORIZED,
    InvalidToken: status.HTTP_401_UNAUTHORIZED,
    ExpiredToken: status.HTTP_401_UNAUTHORIZED,
    MismatchedAccessToken: status.HTTP_401_UNAUTHORIZED,
    InvalidCredentials: status.HTTP_401_UNAUTHORIZED,
    AccessTokenRequired: status.HTTP_401_UNAUTHORIZED,
    RefreshTokenRequired: status.HTTP_401_UNAUTHORIZED,
}


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, unknown_exception_handler)

    app.add_exception_handler(AppError, error_handler(500))
    for exceptions in (_USER_EXC, _TASK_EXC, _TASK_LIST_EXC, _AUTH_EXC):
        for exc_type, status_code in exceptions.items():
            app.add_exception_handler(exc_type, error_handler(status_code))


def error_handler(status_code: int) -> Callable[..., Awaitable[JSONResponse]]:
    return functools.partial(app_error_handler, status_code=status_code)


async def app_error_handler(request: Request, err: AppError, status_code: int) -> JSONResponse:
    logger.error("Unexpected app error", exc_info=err, extra={"error": err})

    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData.from_error(err, status_code),
        status_code=status_code,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status_code: int,
) -> JSONResponse:
    # logger.error("Handle error", exc_info=err, extra={"error": err})
    return JSONResponse(
        ErrorResponse(error=err_data).model_dump(mode="json"),
        status_code=status_code,
    )


async def unknown_exception_handler(_: Request, err: Exception) -> JSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return JSONResponse(
        ErrorResponse(error=ErrorData()).model_dump(mode="json"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
