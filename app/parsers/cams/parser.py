from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.parsers.base import BaseCASParser, ParserMatch, RawCASResult
from app.parsers.shared.state_machine import CASStateMachine


class CAMSParser(BaseCASParser):
    provider = Provider.CAMS

    def can_parse(self, document: ExtractedDocument) -> ParserMatch:
        return ParserMatch(provider=self.provider, confidence=1 if "cams" in document.text.lower() else 0)

    def parse(self, document: ExtractedDocument) -> RawCASResult:
        # Layout-specific state transitions will be added only with approved fixtures.
        machine = CASStateMachine()
        machine.transition(machine.state)
        return RawCASResult(provider=self.provider, warnings=["CAMS layout requires a real regression fixture"])
