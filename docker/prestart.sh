export SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@database:${MYSQL_PORT}/backend"
export PATH=$(pwd):$PATH
export PYTHONPATH=$(pwd)
export APP_MODULE=app:app

echo "backend's database: '${SQLALCHEMY_DATABASE_URL}'"
echo "path: '${PATH}'"
echo "pythonpath: '${PYTHONPATH}'"
echo "app_module: '${APP_MODULE}'"

if [ -z "$MYSQL_PORT" ]; then
    echo "Must provide MYSQL_PORT in environment" 1>&2
    exit 2;
fi

# Wait for database up
./wait-for-it.sh -t 30 "database:${MYSQL_PORT}"

# Show settings for debugging purposes
python -c "from app.core.config import settings;print(repr(settings))"

# Create the database
python ./scripts/ensure-database.py

# Run migrations
alembic upgrade head

python ./scripts/create-first-admin.py
