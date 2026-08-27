from abc import ABC, abstractmethod

from app.models.statement import Statement
from app.parsers.base import RawCASResult


class CASNormalizer(ABC):
    @abstractmethod
    def normalize(self, result: RawCASResult) -> Statement:
        ...
