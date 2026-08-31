from pathlib import Path

from app.core.config import Settings
from app.extractors.strategy import ExtractionStrategy
from app.models.document import ExtractedDocument, ExtractedPage


class DummyExtractor:
    def __init__(self, document: ExtractedDocument) -> None:
        self.document = document

    def extract(self, path: Path) -> ExtractedDocument:
        return self.document


def test_extraction_strategy_uses_ocr_when_enabled_and_primary_is_low_quality() -> None:
    low_quality = ExtractedDocument(
        pages=[ExtractedPage(page_number=1, raw_text="bad")],
        extraction_method="pdfplumber",
    )
    high_quality = ExtractedDocument(
        pages=[ExtractedPage(page_number=1, raw_text="This is a valid extracted statement with enough text for quality checks and quality scoring.")],
        extraction_method="ocr",
    )

    strategy = ExtractionStrategy(
        DummyExtractor(low_quality),
        DummyExtractor(high_quality),
        Settings(ocr_enabled=True),
        ocr_extractor=DummyExtractor(high_quality),
    )

    result = strategy.extract(Path("statement.pdf"))

    assert result.extraction_method == "ocr"
    assert result.text.strip()


def test_extraction_strategy_passes_password_to_extractors() -> None:
    class PasswordAwareExtractor:
        def __init__(self) -> None:
            self.passwords: list[str | None] = []

        def extract(self, path: Path, password: str | None = None) -> ExtractedDocument:
            self.passwords.append(password)
            return ExtractedDocument(
                pages=[ExtractedPage(page_number=1, raw_text="CAMS Consolidated Account Statement with enough text to pass the quality threshold")],
                extraction_method="pdfplumber",
            )

    primary = PasswordAwareExtractor()
    fallback = PasswordAwareExtractor()
    strategy = ExtractionStrategy(primary, fallback, Settings(ocr_enabled=False))

    strategy.extract(Path("statement.pdf"), password="secret")

    assert primary.passwords == ["secret"]
