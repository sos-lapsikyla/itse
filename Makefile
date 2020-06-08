run:
	uvicorn itse:app

lint:
	poetry run black itse
	poetry run flake8
	poetry run mypy -p itse
safety-check:
	poetry run safety check
