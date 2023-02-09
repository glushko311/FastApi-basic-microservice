# Init migration structure 
alembic init migration

# Create migrations in migrations/versions folder
alembic revision --autogenerate -m 'comment'

# Upgrade/downgrade to version
alembic upgrade 7d20a58b4d4a
alembic downgrade 7d20a58b4d4a

