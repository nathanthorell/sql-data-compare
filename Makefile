.PHONY: all install test lint coverage clean run format

all: install lint test

install:
	pip install -e ".[dev]"

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

run:
	python -m sql_data_compare.main
