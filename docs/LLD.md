# Low-Level Design

The `app` package separates API, orchestration, extraction, classification, provider parsers, normalization, validation, confidence, and repositories. `DocumentExtractor`, `BaseCASParser`, `ParserRegistry`, `SchemeResolver`, and `ParseRepository` are the principal extension interfaces.

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Service
  participant Extractor
  participant Classifier
  participant Parser
  Client->>API: POST /v1/parse (PDF)
  API->>Service: temporary path
  Service->>Extractor: extract(path)
  Extractor-->>Service: ExtractedDocument
  Service->>Classifier: classify(document)
  Classifier-->>Service: ProviderDetection
  Service->>Parser: parse(document)
  Parser-->>Service: RawCASResult
  Service-->>API: canonical partial result
```

Provider-specific layout code belongs under `app/parsers/cams` or `app/parsers/kfintech`; shared numeric/date/state utilities belong under `shared`. Real fixture-driven state transitions are intentionally pending sample PDFs.
