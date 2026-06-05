from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import SecretStr
import os


class Settings(BaseSettings):
    app_name: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: SecretStr
    debug: bool = False
    db_url: str

    # def db_url(self) -> str:
    #     return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'stg')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
