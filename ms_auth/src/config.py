from pathlib import Path
from typing import ClassVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    SERVICE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: SecretStr
    debug: bool = False
    db_url: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    SMS_PROVIDER: str

    BOT_TOKEN: str
    CHAT_ID: str

    CELERY_BROKER_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=SERVICE_DIR / ".env.config",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
