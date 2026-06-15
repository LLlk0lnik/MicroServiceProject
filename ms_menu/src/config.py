from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import SecretStr
import os
from pathlib import Path
from typing import ClassVar

class Settings(BaseSettings):

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: SecretStr
    db_url: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / f".env.{os.getenv('APP_ENV', 'stg')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
