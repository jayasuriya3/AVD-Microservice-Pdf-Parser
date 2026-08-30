from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class DematHolding(BaseModel):
    isin: str
    security_name: str | None = None
    trading_symbol: str | None = None
    quantity: Decimal
    market_price: Decimal | None = None
    current_value: Decimal | None = None


class DematTransaction(BaseModel):
    date: date
    isin: str | None = None
    description: str | None = None
    credit_units: Decimal | None = None
    debit_units: Decimal | None = None
    closing_balance: Decimal | None = None


class DematAccount(BaseModel):
    depository: str
    dp_name: str | None = None
    dp_id: str | None = None
    client_id: str | None = None
    holdings: list[DematHolding] = Field(default_factory=list)
    transactions: list[DematTransaction] = Field(default_factory=list)
