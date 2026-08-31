from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "cas-parser"
    version: str = "0.1.0"
    environment: str = "development"
    max_upload_size_bytes: int = 25 * 1024 * 1024
    min_extracted_characters: int = 40
    reconciliation_tolerance: str = "0.05"

    ocr_enabled: bool = False
    ml_classification_enabled: bool = False
    async_job_processing_enabled: bool = False

    pdf_extractor_backend: str = "pdfplumber+fitz"
    ocr_backend: str = "tesseract"
    ml_backend: str = "scikit-learn"
    job_queue_backend: str = "celery"

    model_config = SettingsConfigDict(env_prefix="CAS_PARSER_", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
