#!/usr/bin/env bash
set -euo pipefail

echo "Starting PostgreSQL..."
docker compose up -d db
echo "Waiting for database to be ready..."
until docker compose exec db pg_isready -U postgres > /dev/null 2>&1; do
    sleep 1
done
echo "Database ready."

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting server..."
uv run uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
