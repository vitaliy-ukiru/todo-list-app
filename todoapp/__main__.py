import asyncio
import logging

from todoapp.common.settings import Config
from todoapp.infra.di import init_di_builder, setup_di_builder, DiScope
from todoapp.infra.di.main import setup_di_builder_config
from todoapp.infra.mediator import init_mediator, setup_mediator

logger = logging.getLogger(__name__)


async def main():
    config = Config()
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Launch app", extra={"config": config})
    di_builder = init_di_builder()
    setup_di_builder(di_builder)
    setup_di_builder_config(di_builder, config)

    async with di_builder.enter_scope(DiScope.APP) as di_state:
        mediator = await di_builder.execute(init_mediator, DiScope.APP, state=di_state)
        setup_mediator(mediator)


if __name__ == '__main__':
    asyncio.run(main())
