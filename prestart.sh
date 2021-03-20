export SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@database:${MYSQL_PORT}/backend"
echo "backend's database: '${SQLALCHEMY_DATABASE_URL}'"

if [ -z "$MYSQL_PORT" ]; then
    echo "Must provide MYSQL_PORT in environment" 1>&2
    exit 2;
fi

python -c "from app.core.config import settings;print(repr(settings))"

./wait-for-it.sh -t 30 "database:${MYSQL_PORT}"

# Run migrations
alembic upgrade head

python ./scripts/ensure-database.py
python ./scripts/create-first-admin.py
