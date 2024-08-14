from fastapi import FastAPI, APIRouter

from .auth import auth_router
from .base import base_router
from .healthcheck import healthcheck_router
from .task import task_router
from .task_list import task_list_router
from .user import user_router


def _get_api_router() -> APIRouter:
    api_router = APIRouter(prefix="/api")
    api_router.include_router(healthcheck_router)
    api_router.include_router(user_router)
    api_router.include_router(auth_router)
    api_router.include_router(task_router)
    api_router.include_router(task_list_router)
    return api_router

def setup_controllers(app: FastAPI):
    app.include_router(base_router)
    app.include_router(_get_api_router())
