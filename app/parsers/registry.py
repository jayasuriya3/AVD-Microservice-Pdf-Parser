from app.core.exceptions import UnknownProviderError
from app.models.enums import Provider
from app.parsers.base import BaseCASParser


class ParserRegistry:
    def __init__(self, parsers: list[BaseCASParser] | None = None) -> None:
        self._parsers = {parser.provider: parser for parser in parsers or []}

    def register(self, parser: BaseCASParser) -> None:
        self._parsers[parser.provider] = parser

    def get_parser(self, provider: Provider) -> BaseCASParser:
        try:
            return self._parsers[provider]
        except KeyError as exc:
            raise UnknownProviderError from exc
