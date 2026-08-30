from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.demat import DematAccount
from app.models.enums import Provider


class ProviderDetection(BaseModel):
    name: Provider
    confidence: Decimal = Field(ge=0, le=1)
    signals: list[str] = Field(default_factory=list)


class StatementMetadata(BaseModel):
    provider: Provider
    statement_date: date | None = None
    generated_date: date | None = None


class Investor(BaseModel):
    name: str | None = None
    pan_masked: str | None = None


class Statement(BaseModel):
    parse_id: UUID
    status: str
    provider: ProviderDetection
    statement: StatementMetadata
    investor: Investor
    folios: list[object] = Field(default_factory=list)
    demat_accounts: list[DematAccount] = Field(default_factory=list)
    validation: object | None = None
    confidence: object | None = None
