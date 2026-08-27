from pydantic import BaseModel, Field


class ExtractionQuality(BaseModel):
    sufficient: bool
    character_count: int
    page_count: int
    reasons: list[str] = Field(default_factory=list)
