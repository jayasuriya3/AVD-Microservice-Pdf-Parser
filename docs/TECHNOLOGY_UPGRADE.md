# Open-Source Technology Upgrade

## Overview

This document records the technology upgrades applied to the CAS parser so the project can evolve from a lightweight rule-based service into a more robust open-source document-processing workflow.

The current codebase already includes a FastAPI foundation, PDF extraction utilities, and provider classification rules. These upgrades extend the architecture with optional OCR fallback, ML-assisted classification, and configuration-driven open-source tooling for production use.

---

## Goals

The upgrade aims to:

- support scanned or low-quality PDFs using OCR fallback
- keep the existing provider detection logic as a safe default
- enable optional ML classification without forcing dependency installation
- make the stack configurable for open-source production environments
- keep backward compatibility with current parsing flows

---

## Architectural Changes

### 1. Configuration-driven feature flags

The settings object now includes explicit feature toggles in [app/core/config.py](../app/core/config.py):

- `ocr_enabled`
- `ml_classification_enabled`
- `async_job_processing_enabled`
- backend selectors for PDF extraction, OCR, ML, and queue processing

This allows the application to enable only the features required in a given environment.

### 2. OCR fallback in extraction strategy

The extraction flow in [app/extractors/strategy.py](../app/extractors/strategy.py) now supports an OCR fallback path when the primary extraction result is weak or insufficient.

The logic is:

1. extract using the primary extractor
2. evaluate extraction quality
3. if text quality is insufficient and OCR is enabled, run OCR
4. if OCR output is valid, accept it
5. otherwise use the fallback extractor
6. raise a low-quality extraction error only when all paths fail

This gives the parser a more resilient extraction process for imperfect PDFs.

### 3. Tesseract-based OCR extractor

A new extractor class, [app/extractors/ocr_extractor.py](../app/extractors/ocr_extractor.py), provides an open-source OCR fallback using Tesseract.

It is intentionally optional and does not replace the primary parsing logic. Instead, it acts as a safety net when the source PDF is scanned, ambiguous, or low-quality.

### 4. Optional ML classifier

The new classifier in [app/classifier/ml_classifier.py](../app/classifier/ml_classifier.py) provides a machine-learning alternative to the rule-based provider detection.

The behavior is:

- if `scikit-learn` is available, use TF-IDF + logistic regression to classify provider text
- if the dependency is missing, fall back to the existing provider rules
- if the confidence is below the configured minimum, fall back to the rule engine

This keeps the system practical for dev and local setups without introducing a hard dependency.

---

## Open-Source Tooling Added

The project dependency file now includes optional groups for:

- OCR: `pytesseract`, `rapidocr-onnxruntime`
- ML: `scikit-learn`, `sentence-transformers`
- workers: `celery`, `redis`
- database: `psycopg[binary]`
- monitoring: `prometheus-client`, `opentelemetry-api`

This is captured in [pyproject.toml](../pyproject.toml).

---

## Why This Upgrade Is Useful

This project processes mutual-fund statement PDFs where the source documents can vary significantly in quality. In practice, many PDFs are:

- scanned or partly rasterized
- printed using low-contrast layouts
- inconsistent across providers
- missing text in some sections

The upgraded architecture improves resilience without abandoning the deterministic rule-based parser that already works for known patterns.

---

## Validation Coverage

The project now includes focused tests covering:

- configuration flags in [tests/unit/test_config.py](../tests/unit/test_config.py)
- OCR-aware extraction in [tests/unit/test_extraction_strategy.py](../tests/unit/test_extraction_strategy.py)
- classifier fallback behavior in [tests/unit/test_classifier.py](../tests/unit/test_classifier.py)

This ensures the new optional capabilities remain safe and backwards-compatible.

---

## Recommended Future Roadmap

The next natural upgrades are:

1. async job processing with Celery + Redis
2. PostgreSQL persistence for parse results
3. stronger confidence weighting and validation rules
4. OCR + ML pipeline tuning for real statement fixtures
5. monitoring with Prometheus and OpenTelemetry

---

## Summary

The system now supports a hybrid, open-source-first approach:

- deterministic extraction for standard PDFs
- OCR fallback for scanned documents
- optional ML classification when dependency support is available
- future-ready infrastructure for async processing and monitoring

This keeps the project practical for local development while establishing a path toward production-grade document intelligence.
