import logging

import uvicorn
from di import ScopeState
from didiator import Mediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import FastAPI

from todoapp.common.settings import Config
from todoapp.presentation.api.controllers import setup_controllers
from todoapp.presentation.api.controllers.exceptions import setup_exception_handlers
from todoapp.presentation.api.providers import setup_providers


def init_api(
    mediator: Mediator,
    di_builder: DiBuilder,
    di_state: ScopeState | None = None,
    debug: bool = __debug__,
) -> FastAPI:
    app = FastAPI(
        debug=debug,
        title="ToDo App",
        version="0.0.1",
    )
    setup_providers(app, mediator, di_builder, di_state)
    setup_controllers(app)
    setup_exception_handlers(app)
    return app


async def run_api(app: FastAPI, config: Config) -> None:
    config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
        log_level=logging.INFO,
        log_config=None,
        server_header=False,
        use_colors=True,
        reload=True,
    )
    server = uvicorn.Server(config)
    logging.info("Running API")
    await server.serve()
