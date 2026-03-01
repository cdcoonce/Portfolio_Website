.PHONY: test test-js test-py test-a11y test-e2e test-visual lint check

test: test-js test-py

test-js:
	npm test

test-py:
	uv run pytest -m "not slow"

test-a11y:
	uv run pytest -m a11y

test-e2e:
	uv run pytest -m e2e

test-visual:
	uv run pytest -m slow

lint:
	npm run lint

check: lint test
	@echo "All checks passed."
