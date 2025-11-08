.PHONY: help install run_test test_only linter

help:
	@echo "Makefile commands:"
	@echo "  install      - Install dependencies"
	@echo "  run_test     - Run all tests"
	@echo "  test_only    - Run tests with 'only' marker"
	@echo "  linter       - Run code linters"

install:
	pip install -r requirements.txt

run_test:
	python -m pytest -v

test_only:
	python -m pytest -v -m only

linter:
	black .
	isort .
	flake8
