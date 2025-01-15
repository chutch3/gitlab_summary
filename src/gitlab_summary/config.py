import os
from pydantic import BaseSettings, Field
from typing import Optional


class AppConfig(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    GITLAB_URL: str = Field(default="https://gitlab.com", env="GITLAB_URL")
    GITLAB_TOKEN: str = Field(..., env="GITLAB_TOKEN")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    DATE_RANGE_START: Optional[str] = Field(None, env="DATE_RANGE_START")
    DATE_RANGE_END: Optional[str] = Field(None, env="DATE_RANGE_END")
    GITLAB_GROUP_ID: Optional[str] = Field(None, env="GITLAB_GROUP_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config() -> AppConfig:
    """
    Initializes and returns an AppConfig from environment variables.
    """
    return AppConfig()
