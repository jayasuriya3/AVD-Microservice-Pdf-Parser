from enum import StrEnum


class Provider(StrEnum):
    CAMS = "CAMS"
    CDSL = "CDSL"
    KFINTECH = "KFINTECH"
    UNKNOWN = "UNKNOWN"


class ParseStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class TransactionType(StrEnum):
    PURCHASE = "PURCHASE"
    SIP = "SIP"
    REDEMPTION = "REDEMPTION"
    SWITCH_IN = "SWITCH_IN"
    SWITCH_OUT = "SWITCH_OUT"
    DIVIDEND = "DIVIDEND"
    DIVIDEND_REINVESTMENT = "DIVIDEND_REINVESTMENT"
    UNKNOWN = "UNKNOWN"


class ValidationSeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
