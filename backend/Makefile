.PHONY: run test lint format typecheck

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app
