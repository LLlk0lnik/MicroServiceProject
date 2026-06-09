from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import SecretStr
import os
from pathlib import Path
from typing import ClassVar


class Settings(BaseSettings):

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent

    app_name: str
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

    CELERY_BROKER_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / f".env.{os.getenv('APP_ENV', 'stg')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
