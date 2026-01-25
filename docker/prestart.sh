#!/usr/bin/env bash

echo "FastAPI Prestart Script Running"

DB_USER=$(python -c "from urllib.parse import urlparse; print(urlparse('${DATABASE_URL}').username)")
DB_PASSWORD=$(python -c "from urllib.parse import urlparse; print(urlparse('${DATABASE_URL}').password)")
DB_NAME=$(python -c "from urllib.parse import urlparse; print(urlparse('${DATABASE_URL}').path[1:])")
DB_HOST=$(python -c "from urllib.parse import urlparse; print(urlparse('${DATABASE_URL}').hostname)")

if [ ! -z "$IS_DEV" ]; then
  DB_HOST=$(python -c "from urllib.parse import urlparse; print(urlparse('${DATABASE_URL}').netloc.split('@')[-1]);")
  if [ ! -z "$DB_HOST" ]; then
    while ! nc -zv ${DB_HOST} 5432  > /dev/null 2> /dev/null; do
      echo $DATABASE_URL
      echo "Waiting for postgres to be available at host '${DB_HOST}'"
      sleep 1
    done
  fi
fi

echo "Run Database Migrations"
python -m alembic upgrade head


if [ -f "./f1-db-dump.sql" ]; then
    echo "Seeding data from f1-db-dump.sql..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f ./f1-db-dump.sql
fi


if [ ! -z "$CREATE_TEST_DATA" ]; then
  echo "Creating test data..."
  python -m f1_api.cli test-data
fi

