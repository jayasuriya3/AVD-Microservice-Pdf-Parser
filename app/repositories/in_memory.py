from uuid import UUID

from app.models.statement import Statement
from app.repositories.base import ParseRepository


class InMemoryParseRepository(ParseRepository):
    def __init__(self) -> None:
        self._results: dict[UUID, Statement] = {}

    def save(self, result: Statement) -> None:
        self._results[result.parse_id] = result

    def get(self, parse_id: UUID) -> Statement | None:
        return self._results.get(parse_id)
