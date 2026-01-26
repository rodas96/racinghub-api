#!/usr/bin/env bash
set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

DATABASE_URL="${DATABASE_URL:-postgresql://main:main12345@localhost:5432/main}"

OUT_DIR="f1_api/models"
mkdir -p "$OUT_DIR"

echo "Generating SQLAlchemy models from $DATABASE_URL into $OUT_DIR..."

sqlacodegen "$DATABASE_URL" --outfile "$OUT_DIR/models.py"

echo "Done!"
