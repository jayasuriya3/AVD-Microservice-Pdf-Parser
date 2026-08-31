from functools import lru_cache

from app.application.parse_service import ParseService
from app.classifier.cams_rules import CAMSRules
from app.classifier.kfintech_rules import KFintechRules
from app.classifier.provider_classifier import ProviderClassifier
from app.core.config import get_settings
from app.extractors.ocr_extractor import TesseractOCRExtractor
from app.extractors.pdfplumber_extractor import PdfPlumberExtractor
from app.extractors.pymupdf_extractor import PyMuPDFExtractor
from app.extractors.strategy import ExtractionStrategy
from app.parsers.cams import CAMSParser
from app.parsers.kfintech import KFintechParser
from app.parsers.registry import ParserRegistry
from app.repositories.in_memory import InMemoryParseRepository


@lru_cache
def get_parse_service() -> ParseService:
    settings = get_settings()
    extraction_strategy = ExtractionStrategy(
        PdfPlumberExtractor(),
        PyMuPDFExtractor(),
        settings,
        ocr_extractor=TesseractOCRExtractor() if settings.ocr_enabled else None,
    )
    return ParseService(
        extraction_strategy,
        ProviderClassifier([CAMSRules(), KFintechRules()]),
        ParserRegistry([CAMSParser(), KFintechParser()]),
    )


@lru_cache
def get_repository() -> InMemoryParseRepository:
    return InMemoryParseRepository()
