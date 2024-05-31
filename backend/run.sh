#!/bin/bash

poetry run python3 main.py &
poetry run celery -A src.services.celery_service:celery worker -l info --concurrency=2