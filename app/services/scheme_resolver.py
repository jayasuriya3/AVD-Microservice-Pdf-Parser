from abc import ABC, abstractmethod
from decimal import Decimal

from pydantic import BaseModel


class SchemeResolution(BaseModel):
    normalized_scheme_name: str
    scheme_code: str | None = None
    confidence: Decimal = Decimal("0")


class SchemeResolver(ABC):
    @abstractmethod
    def resolve(self, raw_scheme_name: str) -> SchemeResolution:
        ...


class LocalSchemeResolver(SchemeResolver):
    def resolve(self, raw_scheme_name: str) -> SchemeResolution:
        return SchemeResolution(normalized_scheme_name=raw_scheme_name, confidence=Decimal("0.30"))
