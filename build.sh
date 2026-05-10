#!/usr/bin/env bash
# build.sh - Render build script for Grodiur Django project
set -o errexit

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Seeding default categories..."
python seed_db.py

echo "==> Build complete!"
