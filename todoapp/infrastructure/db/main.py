from collections.abc import AsyncGenerator

from sqlalchemy import URL, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncConnection
)

from todoapp.common.settings import DatabaseConfig


def config_to_url(cfg: DatabaseConfig) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=cfg.username,
        password=cfg.password.get_secret_value() if cfg.password else None,
        database=cfg.database,
        host=cfg.host,
        port=cfg.port,
    )


async def build_sa_engine(db_config: DatabaseConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        config_to_url(db_config),
        echo=False,
    )

    yield engine

    await engine.dispose()


async def ping_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        conn: AsyncConnection = conn
        await conn.execute(select(1))


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
