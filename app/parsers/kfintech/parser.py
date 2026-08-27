from app.models.document import ExtractedDocument
from app.models.enums import Provider
from app.parsers.base import BaseCASParser, ParserMatch, RawCASResult
from app.parsers.shared.state_machine import CASStateMachine


class KFintechParser(BaseCASParser):
    provider = Provider.KFINTECH

    def can_parse(self, document: ExtractedDocument) -> ParserMatch:
        return ParserMatch(provider=self.provider, confidence=1 if "kfintech" in document.text.lower() else 0)

    def parse(self, document: ExtractedDocument) -> RawCASResult:
        machine = CASStateMachine()
        machine.transition(machine.state)
        return RawCASResult(provider=self.provider, warnings=["KFintech layout requires a real regression fixture"])
