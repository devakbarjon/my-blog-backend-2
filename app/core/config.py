from pydantic_settings import BaseSettings
import os

ENV = os.getenv("ENV", "development")  # default to development


class Settings(BaseSettings):
    app_name: str = "My Blog 2.0"
    database_url: str
    environment: str = ENV

    class Config:
        env_file = f".env.{ENV}"  # loads .env.development or .env.production


settings = Settings()