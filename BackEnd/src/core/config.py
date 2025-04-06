from pydantic_settings import BaseSettings
from pydantic import Field
import os
from typing import Optional


class Settings(BaseSettings):
    # API Configurations
    api_title: str = Field(..., env="API_TITLE")
    api_description: str = Field(..., env="API_DESCRIPTION")
    api_version: str = Field(..., env="API_VERSION")

    # Security settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRY_MINUTES: int = Field(..., env="ACCESS_TOKEN_EXPIRY_MINUTES")

    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # EGmini Api Key
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    class Config:
        env_file = "E:\Bhashasutra\BackEnd\src\.env"
        env_file_encoding = "utf-8"


# Initialize settings instance
settings = Settings()


# Dependency Injection Function
def get_settings() -> Settings:
    return settings
