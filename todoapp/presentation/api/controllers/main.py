from fastapi import FastAPI

from .auth import auth_router
from .healthcheck import healthcheck_router
from .user import user_router


def setup_controllers(app: FastAPI):
    app.include_router(healthcheck_router)
    app.include_router(user_router)
    app.include_router(auth_router)
