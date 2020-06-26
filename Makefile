run:
	uvicorn itse:app

lint:
	poetry run black itse
	poetry run black tests
	poetry run flake8
	poetry run mypy -p itse
	poetry run mypy -p tests

test:
	poetry run pytest tests/

tc:
	poetry run mypy -p itse


safety-check:
	poetry run safety check
