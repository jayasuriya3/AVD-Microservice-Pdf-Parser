from abc import ABC, abstractmethod

from app.models.statement import Statement
from app.models.validation import ValidationIssue


class Validator(ABC):
    @abstractmethod
    def validate(self, statement: Statement) -> list[ValidationIssue]:
        ...
