.PHONY: help install run_test test_only linter test

help:
	@echo "Makefile commands:"
	@echo "  install      - Install dependencies using Poetry"
	@echo "  run_test     - Run all tests"
	@echo "  test_only    - Run tests with 'only' marker"
	@echo "  linter       - Run code linters"
	@echo "  test         - Run all tests in quiet mode"

install:
	poetry install

run_test:
	poetry run pytest -v

test_only:
	poetry run pytest -v -m only

linter:
	poetry run black .
	poetry run isort .
	poetry run flake8

test:
	poetry run pytest -q
