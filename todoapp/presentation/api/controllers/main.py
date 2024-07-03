from fastapi import FastAPI

from .auth import auth_router
from .base import base_router
from .healthcheck import healthcheck_router
from .task import task_router
from .task_list import task_list_router
from .user import user_router


def setup_controllers(app: FastAPI):
    app.include_router(base_router)
    app.include_router(healthcheck_router)
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(task_router)
    app.include_router(task_list_router)
