.PHONY: test

test:
	pytest --cov=ncss_api --cov=tests tests/
