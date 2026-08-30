from decimal import Decimal

from app.classifier.base import ProviderRule
from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.models.statement import ProviderDetection


class CDSLRules(ProviderRule):
    provider = Provider.CDSL

    def score(self, document: ExtractedDocument) -> ProviderDetection:
        text = document.text.lower()
        signals: list[str] = []
        score = 0
        if "central depository services" in text or "cdsl" in text:
            score += 70
            signals.append("cdsl_issuer_found")
        if "cas id:" in text:
            score += 30
            signals.append("cas_id_found")
        return ProviderDetection(
            name=Provider.CDSL,
            confidence=Decimal(min(score, 100)) / 100,
            signals=signals,
        )
