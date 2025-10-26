from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/ai_image_lab"
    secret_key: str
    access_token_expire_minutes: int = 30
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()