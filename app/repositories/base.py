from abc import ABC, abstractmethod
from uuid import UUID

from app.models.statement import Statement


class ParseRepository(ABC):
    @abstractmethod
    def save(self, result: Statement) -> None:
        ...

    @abstractmethod
    def get(self, parse_id: UUID) -> Statement | None:
        ...
