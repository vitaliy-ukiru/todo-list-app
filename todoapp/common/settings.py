__all__ = (
    "Config",
    "DatabaseConfig",
)
from typing import Annotated

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


ENV_FILE = ".env"
EXTRA = "ignore"


def _model_config(prefix: str = "") -> SettingsConfigDict:
    return SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        env_prefix=prefix,
        extra="ignore",
        case_sensitive=False,
    )

class DatabaseConfig(BaseSettings):
    password: SecretStr | None = None
    username: str
    database: str
    host: str | None = None
    port: int | None = None

    model_config = _model_config("db_")


class Config(BaseSettings):
    db: Annotated[DatabaseConfig, Field(default_factory=DatabaseConfig)]
    host: str = "localhost"
    port: int = 8000

    model_config = _model_config()
