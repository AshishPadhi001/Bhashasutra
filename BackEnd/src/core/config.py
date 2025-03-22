# src/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Security settings
    SECRET_KEY: str = "Alpha4Beta*Gamma^123Delta!Echo@Foxtrot#Golf%India6Juliet^Kilo_Lima&Mike-22November*Oscar^Papa_Romeo!Sierra!Tango@Uniform-Victor7Whiskey.Xray!Yankee#Zulu$"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRY_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/bhashasutra"
    
    class Config:
        env_file = ".env"

settings = Settings()