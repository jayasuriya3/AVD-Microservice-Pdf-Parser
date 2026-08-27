from abc import ABC, abstractmethod

from app.models.document import ExtractedDocument
from app.models.statement import ProviderDetection


class ProviderRule(ABC):
    provider: str

    @abstractmethod
    def score(self, document: ExtractedDocument) -> ProviderDetection:
        """Return weighted evidence for one provider."""
