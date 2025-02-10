.PHONY: venv all install test lint coverage clean run format

venv:
	python -m venv .venv

all: install lint test

install: venv
	python -m pip install -e ".[dev]"

test:
	pytest

coverage:
	pytest --cov=sql_data_compare --cov-report=xml --cov-report=html --cov-fail-under=80

lint:
	ruff check .
	mypy .

format:
	ruff format .
	ruff check --fix .

clean:
	rm -rf .pytest_cache .coverage htmlcov coverage.xml .mypy_cache dist build
	rm -rf .venv

run:
	python -m sql_data_compare.main