import argparse
from pathlib import Path

from app.core.config import get_settings
from app.extractors.pdfplumber_extractor import PdfPlumberExtractor
from app.extractors.pymupdf_extractor import PyMuPDFExtractor
from app.extractors.strategy import ExtractionStrategy


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect text, coordinates, and tables in a PDF")
    parser.add_argument("path", type=Path)
    parser.add_argument("--password", help="Password for an encrypted PDF")
    args = parser.parse_args()
    document = ExtractionStrategy(PdfPlumberExtractor(), PyMuPDFExtractor(), get_settings()).extract(
        args.path, password=args.password
    )
    print(f"method={document.extraction_method} pages={len(document.pages)} characters={document.character_count}")
    for page in document.pages:
        print(f"\n--- page {page.page_number} ---\n{page.raw_text}")
        print(f"words={len(page.words)} tables={len(page.tables)}")
        for word in page.words:
            print(word.model_dump_json())


if __name__ == "__main__":
    main()
