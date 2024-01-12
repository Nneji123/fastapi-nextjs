import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


def load_env():
    from dotenv import load_dotenv

    env_path = "../.env"
    load_dotenv(env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = (
        f"FastAPI Server - {os.getenv('ENV', 'development').capitalize()}"
    )
    DESCRIPTION: str = "FastAPI + Nextjs Example"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = os.getenv("DATABASE_URI", "postgresql://user:password@postgres:5432/dbname")

    class Config:
        case_sensitive = True


class TestSettings(Settings):
    DATABASE_URI: str = os.getenv("TEST_DATABASE_URI", "sqlite+aiosqlite://")

    class Config:
        case_sensitive = True


settings = Settings()
test_settings = TestSettings()
