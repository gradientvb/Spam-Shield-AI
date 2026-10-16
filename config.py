from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App Configuration
    app_name: str = "SpamShield API"
    debug: bool = True
    version: str = "2.0.0"
    
    # Database
    database_url: str = "postgresql://user:password@localhost/spamshield"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # API Configuration
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
