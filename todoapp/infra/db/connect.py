from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from todoapp.common.settings import DatabaseSettings


def connect_db(cfg: DatabaseSettings, echo: bool = False) -> AsyncEngine:
    engine = create_async_engine(to_dsn(cfg), echo=echo)
    return engine

def new_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)


def to_dsn(cfg: DatabaseSettings) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=cfg.username,
        password=cfg.password.get_secret_value() if cfg.password else None,
        database=cfg.database,
        host=cfg.host,
        port=cfg.port,
    )