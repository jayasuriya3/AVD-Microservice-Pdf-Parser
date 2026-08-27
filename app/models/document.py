from decimal import Decimal

from pydantic import BaseModel, Field


class ExtractedWord(BaseModel):
    text: str
    x0: Decimal
    top: Decimal
    x1: Decimal
    bottom: Decimal


class ExtractedTable(BaseModel):
    rows: list[list[str | None]] = Field(default_factory=list)


class ExtractedPage(BaseModel):
    page_number: int
    raw_text: str = ""
    words: list[ExtractedWord] = Field(default_factory=list)
    tables: list[ExtractedTable] = Field(default_factory=list)


class ExtractedDocument(BaseModel):
    pages: list[ExtractedPage] = Field(default_factory=list)
    metadata: dict[str, str | None] = Field(default_factory=dict)
    extraction_method: str = "unknown"

    @property
    def text(self) -> str:
        return "\n".join(page.raw_text for page in self.pages)

    @property
    def character_count(self) -> int:
        return len(self.text.strip())
