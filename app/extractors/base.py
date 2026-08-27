from abc import ABC, abstractmethod
from pathlib import Path

from app.models.document import ExtractedDocument


class DocumentExtractor(ABC):
    @abstractmethod
    def extract(self, path: Path) -> ExtractedDocument:
        """Extract text, coordinates, tables, and metadata from a document."""
