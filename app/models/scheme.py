from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.transaction import Transaction


class Scheme(BaseModel):
    scheme_name_raw: str
    scheme_name_normalized: str | None = None
    units: Decimal | None = None
    nav: Decimal | None = None
    current_value: Decimal | None = None
    transactions: list[Transaction] = Field(default_factory=list)
    confidence: Decimal = Field(default=Decimal("0"), ge=0, le=1)
