# High-Level Design

## Context
AdvisorDesk sends CAS PDFs to this FastAPI service through an internal API. The service validates files, extracts layout-preserving data, classifies CAMS or KFintech, invokes a provider adapter, normalizes results, validates them, and returns confidence metadata.

```mermaid
flowchart TD
  A[AdvisorDesk API Gateway] --> B[FastAPI CAS Parser]
  B --> C[File validation]
  B --> D[Extraction strategy]
  D --> E[pdfplumber]
  D --> F[PyMuPDF fallback]
  B --> G[Weighted classifier]
  G --> H[CAMS parser]
  G --> I[KFintech parser]
  H --> J[Normalizer]
  I --> J
  J --> K[Validation and confidence]
  K --> L[Canonical result]
```

## Boundaries and security
PDF bytes are accepted only after MIME, signature, and size checks. Temporary files are deleted in `finally`. Raw PDF text, PAN, and financial contents must not be logged. PostgreSQL and queue integrations are deliberately behind interfaces.

## Failure scenarios
Corrupt, encrypted, oversized, unsupported, low-quality, unknown-provider, and parser-failure cases map to structured errors. Low-confidence extraction is never silently treated as complete.

## Observability
JSON logs carry correlation IDs; metrics should later be attached around extraction, provider detection, validation, duration, and outcomes.
