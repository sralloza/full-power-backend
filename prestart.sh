./wait-for-it.sh -t 30 database:3306

# Run migrations
alembic upgrade head

python ./scripts/ensure-database.py
python ./scripts/create-first-admin.py
