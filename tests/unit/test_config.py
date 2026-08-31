from app.core.config import Settings


def test_open_source_feature_flags_default_values() -> None:
    config = Settings()

    assert config.ocr_enabled is False
    assert config.ml_classification_enabled is False
    assert config.async_job_processing_enabled is False
