from fastapi import APIRouter, status

from todoapp.presentation.api.controllers.responses.base import OkStatus, OK_STATUS

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@healthcheck_router.get("/", status_code=status.HTTP_200_OK)
async def get_status() -> OkStatus:
    return OK_STATUS
