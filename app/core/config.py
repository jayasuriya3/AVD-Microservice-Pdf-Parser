from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "cas-parser"
    version: str = "0.1.0"
    environment: str = "development"
    max_upload_size_bytes: int = 25 * 1024 * 1024
    min_extracted_characters: int = 40
    reconciliation_tolerance: str = "0.05"

    model_config = SettingsConfigDict(env_prefix="CAS_PARSER_", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
