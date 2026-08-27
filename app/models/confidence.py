from decimal import Decimal

from pydantic import BaseModel, Field


class ConfidenceResult(BaseModel):
    overall: Decimal = Field(ge=0, le=1)
    sections: dict[str, Decimal] = Field(default_factory=dict)
    fields: dict[str, Decimal] = Field(default_factory=dict)
