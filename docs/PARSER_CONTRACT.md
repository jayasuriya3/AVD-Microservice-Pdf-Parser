# Parser Contract

Extractors return `ExtractedDocument` with pages, raw text, words, coordinates, tables, metadata, and extraction method. Provider parsers implement `BaseCASParser` and return `RawCASResult`.

Normalization emits provider-independent `Statement`, `Folio`, `Scheme`, and `Transaction` models. Financial values use `Decimal`; dates use standard date types. Validation returns issues and warnings without mutating source values. Confidence is represented as provider, section, field, and overall scores.
