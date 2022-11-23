# Variables declarations
message = no_message


# Commands
alembic-start:
	alembic init alembic

alembic-revision:
	alembic revision -m "$(message)"

alembic-autogenerate:
	alembic revision --autogenerate -m "$(message)"

alembic-migrate:
	alembic upgrade head

alembic-history:
	alembic history --verbose

start-app:
	uvicorn main:app --reload
