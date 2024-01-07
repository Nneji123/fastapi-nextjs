import os
import secrets
from typing import Literal


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = f"Webscraper API - {os.getenv('ENV', 'development').capitalize()}"
    DESCRIPTION: str = "A Google Maps Webscraper API Built with FastAPI and SQLModel"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = os.getenv("DATABASE_URI", "sqlite+aiosqlite:///./database.db")


    class Config:
        case_sensitive = True

class TestSettings(Settings):
    class Config:
        case_sensitive = True



def load_env():
    from dotenv import load_dotenv
    env_path = "../.env"
    load_dotenv(env_path)


load_env()
settings = Settings()
test_settings = TestSettings()
