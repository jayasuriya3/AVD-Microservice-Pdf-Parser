from decimal import Decimal

from app.classifier.base import ProviderRule
from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.models.statement import ProviderDetection


class ProviderClassifier:
    def __init__(self, rules: list[ProviderRule], minimum_confidence: float = 0.5) -> None:
        self.rules = rules
        self.minimum_confidence = minimum_confidence

    def classify(self, document: ExtractedDocument) -> ProviderDetection:
        detections = [rule.score(document) for rule in self.rules]
        best = max(detections, key=lambda detection: detection.confidence, default=None)
        if best is None or float(best.confidence) < self.minimum_confidence:
            return ProviderDetection(
                name=Provider.UNKNOWN,
                confidence=Decimal("0"),
                signals=["insufficient_provider_evidence"],
            )
        return best
