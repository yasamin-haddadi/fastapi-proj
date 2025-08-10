from pydantic import AnyUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
from typing import ClassVar

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    REDIS_URL: AnyUrl
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config: ClassVar = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env"
    )

@lru_cache()
def get_settings():
    return Settings()

