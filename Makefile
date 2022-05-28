quickstart: install run_migration run

install:
	poetry install

run:
	poetry run uvicorn drones.main:app

add_migration:
	poetry run alembic revision --autogenerate -m "$(m)"

run_migration:
	poetry run alembic upgrade head

test:
	poetry run pytest --cov=./ --cov-report=xml --cov-report=html -vv

test_no_mock: run_migration
	poetry run pytest --cov=./ --cov-report=xml --cov-report=html -vv --mode=no_mock

cov:
	poetry run python -m http.server -d htmlcov -b 127.0.0.1
