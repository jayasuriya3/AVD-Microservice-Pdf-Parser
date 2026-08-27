from uuid import UUID

from pydantic import BaseModel, Field


class ParseMetadata(BaseModel):
    upload_id: UUID
    firm_id: UUID
    client_id: UUID


class ParseRequest(BaseModel):
    metadata: ParseMetadata
    file_url: str | None = Field(default=None, description="Internal or pre-signed PDF URL")
