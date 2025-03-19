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
    CORS_ORIGINS: Union[List[str], str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
    
    @field_validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[List[str], str]) -> List[str]:
        if isinstance(v, str):
            origins = [i.strip() for i in v.split(",") if i.strip()]
        else:
            origins = [origin for origin in v if origin]
            
        # In production, allow the deployed URL
        if os.getenv("RAILWAY_ENVIRONMENT") == "production":
            origins.append("*")  # Allow all origins in production
            
        # Always include localhost for development
        if "http://localhost:3000" not in origins:
            origins.append("http://localhost:3000")  # React default
        if "http://localhost:8000" not in origins:
            origins.append("http://localhost:8000")  # FastAPI default
            
        # Add FRONTEND_URL if set and not already in the list
        frontend_url = os.getenv("FRONTEND_URL")
        if frontend_url and frontend_url not in origins:
            origins.append(frontend_url)
            
        return origins
    
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
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Server config
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = "0.0.0.0"  # Allow external connections
    
    # Additional fields from .env that might be used
    APP_ENV: str = os.getenv("APP_ENV", "development")
    PRODUCTION: bool = os.getenv("PRODUCTION", "false").lower() == "true"
    REACT_APP_SUPABASE_URL: str = os.getenv("REACT_APP_SUPABASE_URL", "")
    REACT_APP_SUPABASE_ANON_KEY: str = os.getenv("REACT_APP_SUPABASE_ANON_KEY", "")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in .env file
    )


settings = Settings() 