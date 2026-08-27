from pydantic import BaseModel, Field

from app.models.scheme import Scheme


class Folio(BaseModel):
    folio_number: str
    schemes: list[Scheme] = Field(default_factory=list)
