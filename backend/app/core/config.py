"""
Application configuration and settings
"""

from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    APP_NAME: str = Field(default="AI Resume Builder", env="APP_NAME")
    VERSION: str = Field(default="1.0.0", env="VERSION")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")

    # Database
    DATABASE_URL: str = Field(env="DATABASE_URL", description="Database connection URL")

    # Security
    JWT_SECRET: str = Field(env="JWT_SECRET", description="JWT signing secret")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
        ],
        env="ALLOWED_ORIGINS",
        description="CORS allowed origins",
    )

    # LLM / AI
    GROQ_API_KEY: str = Field(
        env="GROQ_API_KEY", description="Groq API key for LLM calls"
    )
    GROQ_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        env="GROQ_MODEL",
        description="Groq model for LLM calls",
    )

    # Vector Embeddings (pgvector)
    EMBEDDING_MODEL: str = Field(
        default="all-MiniLM-L6-v2",
        env="EMBEDDING_MODEL",
        description="Sentence transformer model for embeddings",
    )
    EMBEDDING_DIMENSION: int = Field(
        default=384,
        env="EMBEDDING_DIMENSION",
        description="Dimension of embeddings (384 for all-MiniLM-L6-v2)",
    )

    # Redis & Celery
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL",
        description="Redis connection URL for Celery broker",
    )
    REDIS_BACKEND_URL: str = Field(
        default="redis://localhost:6379/1",
        env="REDIS_BACKEND_URL",
        description="Redis URL for Celery result backend",
    )

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="standard", env="LOG_FORMAT"
    )  # "standard" or "json"

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def effective_log_format(self) -> str:
        """Use JSON format in production, standard in development"""
        return "json" if self.is_production else "standard"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
