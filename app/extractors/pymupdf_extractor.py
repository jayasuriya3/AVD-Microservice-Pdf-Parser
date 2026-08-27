from decimal import Decimal
from pathlib import Path

import fitz

from app.core.exceptions import CorruptedPDFError, EncryptedPDFError
from app.extractors.base import DocumentExtractor
from app.models.document import ExtractedDocument, ExtractedPage, ExtractedWord


class PyMuPDFExtractor(DocumentExtractor):
    def extract(self, path: Path) -> ExtractedDocument:
        try:
            with fitz.open(path) as pdf:
                if pdf.is_encrypted:
                    raise EncryptedPDFError
                pages = []
                for page_number, page in enumerate(pdf, start=1):
                    words = [
                        ExtractedWord(
                            text=str(item[4]),
                            x0=Decimal(str(item[0])), top=Decimal(str(item[1])),
                            x1=Decimal(str(item[2])), bottom=Decimal(str(item[3])),
                        )
                        for item in page.get_text("words")
                    ]
                    pages.append(ExtractedPage(page_number=page_number, raw_text=page.get_text(), words=words))
                return ExtractedDocument(pages=pages, metadata={str(k): str(v) for k, v in pdf.metadata.items()}, extraction_method="pymupdf")
        except EncryptedPDFError:
            raise
        except Exception as exc:
            raise CorruptedPDFError from exc
