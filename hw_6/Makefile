.PHONY: help install run_test test_only linter test

help:
	@echo "Makefile commands:"
	@echo "  install      - Install dependencies using Poetry"
	@echo "  linter       - Run code linters"

install:
	poetry install

linter:
	poetry run black .
	poetry run isort .
	poetry run flake8
