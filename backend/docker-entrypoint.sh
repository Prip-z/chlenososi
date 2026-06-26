#!/bin/sh
set -e

echo "Waiting for postgres..."
until pg_isready -h postgres -U mapuser -p 5432 -d forestmap 2>/dev/null; do
  echo "Postgres unavailable, waiting..."
  sleep 2
done
echo "Postgres is available"

echo "Running migrations..."
alembic upgrade head 2>&1 || echo "Migration warnings/errors (non-fatal)"

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
