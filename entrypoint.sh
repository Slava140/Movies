#!/bin/sh

echo "Применение миграции"
alembic upgrade head

echo "Запуск приложения"
python src/main.py

exec "$@"
