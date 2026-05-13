#!/bin/sh

cd /fastapi_db

# Ждем PostgreSQL
python -c "
import time
import psycopg2
while True:
    try:
        psycopg2.connect('postgresql://blog:blogpass@db:5432/blog')
        print('PostgreSQL is ready!')
        break
    except Exception as e:
        print(f'Waiting for postgres... {e}')
        time.sleep(1)
"

# Запускаем миграции
alembic upgrade head

# Запускаем приложение
cd fastapi_app
exec uvicorn main:app --host 0.0.0.0 --port 8000