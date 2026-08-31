from pathlib import Path

from app.extractors.base import DocumentExtractor
from app.models.document import ExtractedDocument, ExtractedPage


class TesseractOCRExtractor(DocumentExtractor):
    """OCR fallback for scanned or low-quality PDFs using the open-source Tesseract engine."""

    def extract(self, path: Path, password: str | None = None) -> ExtractedDocument:
        try:
            import pytesseract
            from PIL import Image
            import fitz
        except ImportError as exc:  # pragma: no cover - depends on optional OCR install
            raise RuntimeError("OCR dependencies are not installed. Install the 'ocr' optional dependencies.") from exc

        pages: list[ExtractedPage] = []
        with fitz.open(path) as pdf:
            if password:
                decrypted = pdf.authenticate(password)
                if not decrypted:
                    raise EncryptedPDFError
            for page_number, page in enumerate(pdf, start=1):
                image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                image_bytes = image.tobytes("png")
                pil_image = Image.open(__import__("io").BytesIO(image_bytes))
                text = pytesseract.image_to_string(pil_image)
                pages.append(ExtractedPage(page_number=page_number, raw_text=text, words=[], tables=[]))

        return ExtractedDocument(
            pages=pages,
            metadata={"source": "ocr", "engine": "tesseract"},
            extraction_method="ocr",
        )
