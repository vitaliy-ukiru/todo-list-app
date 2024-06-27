import asyncio
import logging

from todoapp.common.settings import Config
from todoapp.infrastructure.di import DiScope, init_di_builder, setup_di_builder
from todoapp.infrastructure.mediator import init_mediator, setup_mediator
from todoapp.presentation.api.main import init_api, run_api

logger = logging.getLogger(__name__)


async def main():
    config = Config()
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Launch app", extra={"config": config})
    di_builder = init_di_builder()

    mediator = init_mediator(di_builder)
    setup_mediator(mediator)

    setup_di_builder(di_builder, config)

    async with di_builder.enter_scope(DiScope.APP) as di_state:
        app = init_api(mediator, di_builder, di_state, debug=False)

        await run_api(app, config)


if __name__ == '__main__':
    asyncio.run(main())
