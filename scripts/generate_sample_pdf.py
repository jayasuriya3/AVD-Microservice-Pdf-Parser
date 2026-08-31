from pathlib import Path

import fitz


def main() -> None:
    path = Path("tests/fixtures/sample_statement.pdf")
    path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "CAMS\n")
    page.insert_text((72, 100), "Consolidated Account Statement")
    page.insert_text((72, 130), "Investor Name: Sample Investor")
    page.insert_text((72, 160), "Folio No: 12345")
    page.insert_text((72, 190), "Scheme: HDFC Balanced Advantage Fund")
    doc.save(path)
    doc.close()
    print(f"Created sample PDF at {path}")


if __name__ == "__main__":
    main()
