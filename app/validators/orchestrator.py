from app.models.validation import ValidationResult


def validate_result() -> ValidationResult:
    return ValidationResult(is_valid=True)
