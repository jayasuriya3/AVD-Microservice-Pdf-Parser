from decimal import Decimal
from pathlib import Path

import pdfplumber

from app.core.exceptions import CorruptedPDFError, EncryptedPDFError
from app.extractors.base import DocumentExtractor
from app.models.document import ExtractedDocument, ExtractedPage, ExtractedTable, ExtractedWord


class PdfPlumberExtractor(DocumentExtractor):
    def extract(self, path: Path, password: str | None = None) -> ExtractedDocument:
        try:
            with pdfplumber.open(path, password=password) as pdf:
                pages: list[ExtractedPage] = []
                for page_number, page in enumerate(pdf.pages, start=1):
                    words = [
                        ExtractedWord(
                            text=str(word["text"]),
                            x0=Decimal(str(word["x0"])),
                            top=Decimal(str(word["top"])),
                            x1=Decimal(str(word["x1"])),
                            bottom=Decimal(str(word["bottom"])),
                        )
                        for word in page.extract_words()
                    ]
                    tables = [ExtractedTable(rows=table) for table in (page.extract_tables() or [])]
                    pages.append(ExtractedPage(page_number=page_number, raw_text=page.extract_text() or "", words=words, tables=tables))
                return ExtractedDocument(pages=pages, metadata=pdf.metadata or {}, extraction_method="pdfplumber")
        except Exception as exc:
            message = str(exc).lower()
            if "password" in message or "encrypt" in message:
                raise EncryptedPDFError from exc
            raise CorruptedPDFError from exc
