#!/bin/sh

alembic upgrade head
python /fastapi_app/main.py