from decimal import Decimal

from app.classifier.base import ProviderRule
from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.models.statement import ProviderDetection


class KFintechRules(ProviderRule):
    provider = Provider.KFINTECH

    def score(self, document: ExtractedDocument) -> ProviderDetection:
        text = document.text.lower()
        score = 0
        signals: list[str] = []
        if "kfintech" in text or "karvy fintech" in text:
            score += 50
            signals.append("provider_name_found")
        if "consolidated account statement" in text:
            score += 30
            signals.append("known_statement_header")
        if "registrar & transfer agent" in text or "folio no" in text:
            score += 20
            signals.append("provider_specific_phrase")
        return ProviderDetection(name=Provider.KFINTECH, confidence=Decimal(min(score, 100)) / 100, signals=signals)
