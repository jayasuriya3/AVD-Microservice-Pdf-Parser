from decimal import Decimal

from app.classifier.base import ProviderRule
from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.models.statement import ProviderDetection


class CAMSRules(ProviderRule):
    provider = Provider.CAMS

    def score(self, document: ExtractedDocument) -> ProviderDetection:
        text = document.text.lower()
        score = 0
        signals: list[str] = []
        if "cams" in text or "computer age management services" in text:
            score += 50
            signals.append("provider_name_found")
        if "consolidated account statement" in text:
            score += 30
            signals.append("known_statement_header")
        if "registrar and transfer agent" in text:
            score += 20
            signals.append("provider_specific_phrase")
        return ProviderDetection(name=Provider.CAMS, confidence=Decimal(min(score, 100)) / 100, signals=signals)
