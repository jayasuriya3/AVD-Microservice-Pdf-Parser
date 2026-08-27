from enum import StrEnum


class ParseState(StrEnum):
    START = "START"
    INVESTOR = "INVESTOR"
    FOLIO = "FOLIO"
    SCHEME = "SCHEME"
    TRANSACTIONS = "TRANSACTIONS"
    VALUATION = "VALUATION"
    END = "END"


class CASStateMachine:
    def __init__(self) -> None:
        self.state = ParseState.START
        self.current_folio: str | None = None
        self.current_scheme: str | None = None

    def transition(self, state: ParseState) -> None:
        self.state = state
