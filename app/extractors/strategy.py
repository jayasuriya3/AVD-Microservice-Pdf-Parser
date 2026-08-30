from pathlib import Path

from app.core.config import Settings
from app.core.exceptions import LowQualityExtractionError
from app.extractors.base import DocumentExtractor
from app.extractors.models import ExtractionQuality
from app.models.document import ExtractedDocument


class ExtractionStrategy:
    def __init__(self, primary: DocumentExtractor, fallback: DocumentExtractor, settings: Settings) -> None:
        self.primary = primary
        self.fallback = fallback
        self.settings = settings

    def extract(self, path: Path, password: str | None = None) -> ExtractedDocument:
        document = self.primary.extract(path, password=password)
        quality = self.quality(document)
        if quality.sufficient:
            return document
        fallback_document = self.fallback.extract(path, password=password)
        if not self.quality(fallback_document).sufficient:
            raise LowQualityExtractionError
        return fallback_document

    def quality(self, document: ExtractedDocument) -> ExtractionQuality:
        reasons: list[str] = []
        if not document.pages:
            reasons.append("no_pages")
        if document.character_count < self.settings.min_extracted_characters:
            reasons.append("insufficient_text")
        return ExtractionQuality(
            sufficient=not reasons,
            character_count=document.character_count,
            page_count=len(document.pages),
            reasons=reasons,
        )
