from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Agent Evaluation System"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./agent_eval.db"
    opengauss_url: str = "postgresql+psycopg2://gaussdb:password@localhost:5432/agent_eval"
    storage_dir: str = "storage"
    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    judge_model_name: str = "deepseek-v3"
    max_upload_size_mb: int = 10
    max_concurrent_jobs: int = 5
    use_mock_judge: bool = True

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def storage_path(self) -> Path:
        return Path(self.storage_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()
