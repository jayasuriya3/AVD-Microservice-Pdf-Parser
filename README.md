# AdvisorDesk CAS Parser

Production-oriented foundation for parsing Indian mutual-fund Consolidated Account Statements (CAS) from CAMS and KFintech into one provider-independent model.

## Local setup

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
make install
make run
```

The OpenAPI UI is available at `http://localhost:8000/docs`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## API examples

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl -X POST http://localhost:8000/v1/parse -F file=@statement.pdf
curl -X POST http://localhost:8000/v1/parse -F file=@statement.pdf -F password='your-password'
curl http://localhost:8000/v1/parses/{parse_id}
```

## Local sample fixture

Generate a sample PDF to exercise the upload and provider-detection flow locally:

```bash
python scripts/generate_sample_pdf.py
curl -X POST http://localhost:8000/v1/parse -F "file=@tests/fixtures/sample_statement.pdf"
```

This file is only a local sample for testing the API contract. It does not represent a real CAMS/KFintech CAS layout yet.

## Current milestone

Implemented:

- FastAPI app, health/readiness, OpenAPI, correlation-ID middleware
- Secure local PDF upload validation and temporary-file cleanup
- pdfplumber extraction with coordinates, tables, and configurable PyMuPDF fallback
- Weighted CAMS/KFintech provider classification
- Common parser contract, registry, state-machine foundation, and provider skeletons
- Decimal-based canonical models, scheme resolver interface, in-memory repository
- Structured JSON logging, Docker, Compose, Ruff, mypy, pytest setup, and architecture docs

Pending real CAS fixtures:

- Layout-specific folio, scheme, valuation, and transaction extraction
- Full validation/reconciliation and field-level confidence rules
- PostgreSQL persistence and external job integration

Do not claim support for a specific CAS layout until an anonymized, permitted PDF is added as a regression fixture. Use `python scripts/inspect_pdf.py path/to/file.pdf` to inspect a sample before implementing its rules.

## Development checks

```bash
make test
make lint
make typecheck
```