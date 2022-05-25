run:
	uvicorn drones.main:app

add_migration:
	alembic revision --autogenerate -m "$(m)"

run_migration:
	alembic upgrade head
