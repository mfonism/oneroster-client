.PHONY: format lint test all

format:
	isort src tests
	black src tests

lint:
	flake8 src tests

test:
	pytest src tests

all: format lint tests
