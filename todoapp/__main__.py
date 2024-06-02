import asyncio
import logging

from todoapp.common.settings import Config
from todoapp.infrastructure.di import DiScope, build_di_builder
from todoapp.infrastructure.mediator import init_mediator, setup_mediator

logger = logging.getLogger(__name__)


async def main():
    config = Config()
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Launch app", extra={"config": config})
    di_builder = build_di_builder(config)

    async with di_builder.enter_scope(DiScope.APP) as di_state:
        mediator = await di_builder.execute(init_mediator, DiScope.APP, state=di_state)
        setup_mediator(mediator)


if __name__ == '__main__':
    asyncio.run(main())
