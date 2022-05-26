run:
	uvicorn drones.main:app

add_migration:
	alembic revision --autogenerate -m "$(m)"

run_migration:
	alembic upgrade head

test:
	poetry run pytest --cov=./ --cov-report=xml --cov-report=html -vv

cov:
	python -m http.server -d htmlcov -b 127.0.0.1
