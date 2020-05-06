lint:
	black -l 80 --check itse/
safety-check:
	poetry run safety check
