from uuid import UUID

from pydantic import BaseModel

from app.models.enums import ParseStatus
from app.models.statement import Statement


class ErrorDetail(BaseModel):
    code: str
    message: str
    retryable: bool = False


class ErrorResponse(BaseModel):
    error: ErrorDetail


class ParseResponse(Statement):
    parse_id: UUID
    status: ParseStatus
