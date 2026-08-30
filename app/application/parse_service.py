from pathlib import Path
from uuid import UUID, uuid4

from app.classifier.provider_classifier import ProviderClassifier
from app.core.exceptions import UnknownProviderError
from app.extractors.strategy import ExtractionStrategy
from app.models.enums import ParseStatus
from app.models.statement import Investor, Statement, StatementMetadata
from app.parsers.registry import ParserRegistry


class ParseService:
    def __init__(self, extractor: ExtractionStrategy, classifier: ProviderClassifier, registry: ParserRegistry) -> None:
        self.extractor = extractor
        self.classifier = classifier
        self.registry = registry

    def parse_file(
        self, path: Path, parse_id: UUID | None = None, password: str | None = None
    ) -> Statement:
        document = self.extractor.extract(path, password=password)
        detection = self.classifier.classify(document)
        if detection.name.value == "UNKNOWN":
            raise UnknownProviderError
        raw = self.registry.get_parser(detection.name).parse(document)
        parse_status = ParseStatus.COMPLETED.value if not raw.warnings else ParseStatus.PARTIAL.value
        return Statement(
            parse_id=parse_id or uuid4(), status=parse_status,
            provider=detection,
            statement=StatementMetadata(provider=detection.name), investor=Investor(name=raw.investor_name),
            folios=[folio.model_dump() for folio in raw.folios],
            demat_accounts=raw.demat_accounts,
            validation={"is_valid": True, "warnings": raw.warnings},
            confidence={"overall": detection.confidence},
        )
