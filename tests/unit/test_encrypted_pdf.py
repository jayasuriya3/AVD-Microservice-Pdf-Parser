from pathlib import Path

import fitz
import pytest

from app.core.exceptions import EncryptedPDFError
from app.extractors.base import DocumentExtractor
from app.extractors.pdfplumber_extractor import PdfPlumberExtractor
from app.extractors.pymupdf_extractor import PyMuPDFExtractor


@pytest.fixture
def encrypted_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "protected.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "CAMS Consolidated Account Statement")
    document.save(
        path,
        encryption=fitz.PDF_ENCRYPT_AES_256,
        owner_pw="owner-password",
        user_pw="statement-password",
    )
    document.close()
    return path


@pytest.mark.parametrize("extractor", [PdfPlumberExtractor(), PyMuPDFExtractor()])
def test_encrypted_pdf_requires_valid_password(
    encrypted_pdf: Path, extractor: DocumentExtractor
) -> None:
    with pytest.raises(EncryptedPDFError):
        extractor.extract(encrypted_pdf)
    with pytest.raises(EncryptedPDFError):
        extractor.extract(encrypted_pdf, password="wrong-password")

    document = extractor.extract(encrypted_pdf, password="statement-password")
    assert "CAMS" in document.text
