class CASParserError(Exception):
    code = "CAS_PARSER_ERROR"
    retryable = False


class UnsupportedDocumentError(CASParserError):
    code = "UNSUPPORTED_DOCUMENT"


class UnknownProviderError(CASParserError):
    code = "UNKNOWN_PROVIDER"


class EncryptedPDFError(CASParserError):
    code = "ENCRYPTED_PDF"


class CorruptedPDFError(CASParserError):
    code = "CORRUPTED_PDF"


class LowQualityExtractionError(CASParserError):
    code = "LOW_QUALITY_EXTRACTION"


class ParserFailureError(CASParserError):
    code = "PARSER_FAILURE"
    retryable = True


class ValidationFailureError(CASParserError):
    code = "VALIDATION_FAILURE"
