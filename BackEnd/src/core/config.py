from pydantic_settings import BaseSettings
from pydantic import Field

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

    # Hugging Face API settings
    huggingface_api_key: str = Field("", env="HUGGINGFACE_API_KEY")
    huggingface_model_id: str = Field("gpt2", env="HUGGINGFACE_MODEL_ID")

    class Config:
        env_file = "E:\Bhashasutra\BackEnd\src\.env"
        env_file_encoding = "utf-8"

# Initialize settings instance
settings = Settings()

# Dependency Injection Function
def get_settings() -> Settings:
    return settings
