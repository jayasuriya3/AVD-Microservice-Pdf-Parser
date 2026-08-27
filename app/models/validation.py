from pydantic import BaseModel, Field

from app.models.enums import ValidationSeverity


class ValidationIssue(BaseModel):
    code: str
    message: str
    severity: ValidationSeverity


class ValidationResult(BaseModel):
    is_valid: bool
    warnings: list[ValidationIssue] = Field(default_factory=list)
