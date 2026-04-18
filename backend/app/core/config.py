from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task Manager"
    secret_key: str = Field("change-me-in-production", alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = Field("sqlite:///./task_manager.db", alias="DATABASE_URL")
    db_connect_max_retries: int = Field(10, alias="DB_CONNECT_MAX_RETRIES")
    db_connect_retry_delay_seconds: float = Field(2.0, alias="DB_CONNECT_RETRY_DELAY_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
