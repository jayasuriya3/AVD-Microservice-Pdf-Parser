.PHONY: install test lint typecheck run

install:
	python -m pip install -e '.[dev]'

test:
	python -m pytest

lint:
	ruff check .

typecheck:
	mypy app

run:
	uvicorn app.main:app --reload
