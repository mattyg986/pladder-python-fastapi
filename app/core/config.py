import os
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Purple Ladder AI Agents"
    
    # Environment
    ENVIRONMENT: str = os.getenv("RAILWAY_ENVIRONMENT", "development")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "1aa28c01dbfb5ad6ad45cb9f6f3f71b18a43d47d10277e8e")
    
    # CORS Settings
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:8000",  # FastAPI default
        os.getenv("FRONTEND_URL", ""),  # From .env
    ]
    
    @field_validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: List[str]) -> Union[List[str], str]:
        # Remove empty strings
        v = [origin for origin in v if origin]
        # In production, allow the deployed URL
        if os.getenv("RAILWAY_ENVIRONMENT") == "production":
            v.append("*")  # Allow all origins in production
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)
    
    # Redis and Celery
    # For Railway, use the REDIS_URL environment variable if available
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Set Celery broker and backend based on environment
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.REDIS_URL
    
    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL
    
    # Database
    # Use DATABASE_URL from Railway if available
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Server config
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = "0.0.0.0"  # Allow external connections
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings() 