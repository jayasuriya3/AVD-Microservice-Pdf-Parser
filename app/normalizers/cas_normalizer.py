from uuid import uuid4

from app.models.enums import ParseStatus
from app.models.statement import Investor, ProviderDetection, Statement, StatementMetadata
from app.parsers.base import RawCASResult


def normalize(result: RawCASResult, detection: ProviderDetection) -> Statement:
    return Statement(parse_id=uuid4(), status=ParseStatus.PARTIAL.value, provider=detection,
                     statement=StatementMetadata(provider=result.provider), investor=Investor(name=result.investor_name),
                     folios=[folio.model_dump() for folio in result.folios],
                     validation={"is_valid": True, "warnings": result.warnings}, confidence={"overall": detection.confidence})
