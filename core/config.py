from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache 

class Settings(BaseSettings):
    """Configuration for the application."""

    # Database settings (Required - app will crash if missing in .env)
    DATABASE_URL: str

    # API settings (Optional - has defaults)
    API_PREFIX: str = "/api/v1"
    APP_NAME: str = "Pro Task Manager"

    # Security (Good to have for later)
    SECRET_KEY: str = "development_secret_key"

    # Modern Pydantic V2 config style
    model_config = SettingsConfigDict(
        env_file=".env.dev", # Changed from .env.dev to .env for standard use
        env_file_encoding="utf-8",
        extra="ignore"   # Ignores extra variables in your .env
    )

@lru_cache
def get_settings():
    """Get the application configuration."""
    return Settings()