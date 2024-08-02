.PHONY: format lint test all

format:
	isort src test
	black src test

lint:
	flake8 src test

test:
	pytest src test

all: format lint test
