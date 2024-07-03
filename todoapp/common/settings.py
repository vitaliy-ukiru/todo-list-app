__all__ = (
    "Config",
    "DatabaseConfig",
    "AuthConfig",
)

from datetime import timedelta
from typing import Annotated

from pydantic import SecretStr, Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

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


class AuthConfig(BaseSettings):
    access_token_expires: Annotated[timedelta, Field(default=timedelta(minutes=5))]
    refresh_token_expires: Annotated[timedelta, Field(default=timedelta(days=30))]

    private_key_path: str
    jwt_alg: Annotated[str, Field(default="RS256")]

    model_config = _model_config("auth_")


class Config(BaseSettings):
    db: Annotated[DatabaseConfig, Field(default_factory=DatabaseConfig)]
    auth: Annotated[AuthConfig, Field(default_factory=AuthConfig)]
    redis_url: Annotated[RedisDsn, Field(default="redis://127.0.0.1:6379")]
    api_host: str = "localhost"
    api_port: int = 8000

    model_config = _model_config()
