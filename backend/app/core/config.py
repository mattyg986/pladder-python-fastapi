import os
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, field_validator, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Purple Ladder AI Agents Platform"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = os.getenv("RAILWAY_ENVIRONMENT", "development")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "1aa28c01dbfb5ad6ad45cb9f6f3f71b18a43d47d10277e8e")
    
    # CORS Settings
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # React dev server alternate port
        "http://localhost:8000",  # Backend dev server
        "http://frontend",        # Frontend container in docker network
        "http://frontend:80",     # Frontend container with port in docker network
        "https://pladder.app",    # Production domain
    ]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            # Handle quoted string with commas
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            # Handle normal comma-separated string
            if "," in v:
                return [i.strip() for i in v.split(",")]
            # Handle single URL
            return [v.strip()]
        elif isinstance(v, list):
            return v
        raise ValueError(f"Invalid CORS_ORIGINS format: {v}")
    
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
    SUPABASE_JWT_SECRET: Optional[str] = None
    
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