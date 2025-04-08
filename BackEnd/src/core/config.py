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

    # Gemini API Key
    GEMINI_API_KEY: Optional[str] = Field(default=None, env="GEMINI_API_KEY")

    # Mail Configuration
    SMTP_USERNAME: str = Field(..., env="SMTP_USERNAME")
    SMTP_PASSWORD: str = Field(..., env="SMTP_PASSWORD")
    SMTP_SERVER: str = Field(..., env="SMTP_SERVER")
    SMTP_PORT: int = Field(..., env="SMTP_PORT")
    SENDER_EMAIL: str = Field(..., env="SENDER_EMAIL")
    MAIL_TLS: bool = Field(..., env="MAIL_TLS")
    MAIL_SSL: bool = Field(..., env="MAIL_SSL")
    USE_CREDENTIALS: bool = Field(..., env="USE_CREDENTIALS")

    class Config:
        env_file = "E:\\Bhashasutra\\BackEnd\\src\\.env"
        env_file_encoding = "utf-8"


# Initialize settings instance
settings = Settings()


# Dependency Injection Function
def get_settings() -> Settings:
    return settings
