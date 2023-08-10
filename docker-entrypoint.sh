#!/bin/sh

# Apply database migrations
echo "Make migrations"
poetry run flask db migrate
poetry run flask db upgrade

echo "Start server"
poetry run python3 entrypoint.py
