#!/bin/bash

echo "Stopping Celery worker..."
pkill -f 'celery -A task_manager worker'

# echo "Stopping Celery Beat..."
# pkill -f 'celery -A task_manager beat'

echo "Stopping Uvicorn server..."
pkill -f 'uvicorn task_manager.asgi:app'

echo "All services stopped."