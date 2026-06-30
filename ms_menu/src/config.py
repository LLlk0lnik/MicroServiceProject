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
    db_url: str
    debug: bool = False
    REDIS_URL: str


    model_config = SettingsConfigDict(
        env_file=SERVICE_DIR / ".env.config",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
