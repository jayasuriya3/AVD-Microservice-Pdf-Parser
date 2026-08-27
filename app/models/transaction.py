from datetime import date as Date
from decimal import Decimal

from pydantic import BaseModel

from app.models.enums import TransactionType


class Transaction(BaseModel):
    date: Date | None = None
    type: TransactionType = TransactionType.UNKNOWN
    amount: Decimal | None = None
    units: Decimal | None = None
    nav: Decimal | None = None
