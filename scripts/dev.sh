#!/usr/bin/env bash
set -euo pipefail

echo "Starting PostgreSQL..."
docker compose up -d db
echo "Waiting for database to be ready..."
MAX_RETRIES=30
count=0
until docker compose exec db pg_isready -U postgres > /dev/null 2>&1; do
    sleep 1
    count=$((count+1))
    if [ $count -ge $MAX_RETRIES ]; then
        echo "Database failed to start within $MAX_RETRIES seconds."
        exit 1
    fi
done
echo "Database ready."

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting server..."
uv run uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
