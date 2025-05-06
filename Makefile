format:
	isort . || true
	black .

lint:
	ruff check . || true
	flake8 .

fix:
	ruff check . --fix

check:
	black --check . || true
	ruff check . --diff
