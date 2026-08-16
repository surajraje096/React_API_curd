import os
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Agent Platform"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/agent_db"
    )
    SQLITE_FALLBACK_URL: str = Field(
        default="sqlite+aiosqlite:///./agent.db"
    )

    # LLM Settings
    OPENAI_API_KEY: str = Field(default="")
    DEFAULT_MODEL: str = Field(default="gpt-4o-mini")
    ENABLE_MOCK_LLM_IF_NO_KEY: bool = True

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = Settings()
