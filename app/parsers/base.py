from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from app.models.demat import DematAccount
from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.models.folio import Folio


class ParserMatch(BaseModel):
    provider: Provider
    confidence: float
    signals: list[str] = Field(default_factory=list)


class RawCASResult(BaseModel):
    provider: Provider
    investor_name: str | None = None
    statement_date: str | None = None
    folios: list[Folio] = Field(default_factory=list)
    demat_accounts: list[DematAccount] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class BaseCASParser(ABC):
    provider: Provider

    @abstractmethod
    def can_parse(self, document: ExtractedDocument) -> ParserMatch:
        ...

    @abstractmethod
    def parse(self, document: ExtractedDocument) -> RawCASResult:
        ...
