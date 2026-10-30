from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg://dormitory:changeme@localhost:5432/dormitory"
    secret_key: str = "development-only-change-me-at-least-32-bytes"
    jwt_issuer: str = "dormitory-api"
    jwt_audience: str = "dormitory-client"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    cors_origins: str = ""

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
