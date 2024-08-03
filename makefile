.PHONY: format lint test all

format:
	isort src tests
	black src tests

lint:
	flake8 src tests

test:
	pytest

all: format lint test
