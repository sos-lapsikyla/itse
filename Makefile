run:
	uvicorn itse:app

lint:
	poetry run black itse
	poetry run flake8
	poetry run mypy -p itse
	poetry run mypy -p tests
safety-check:
	poetry run safety check
