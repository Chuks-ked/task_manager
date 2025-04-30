#!/bin/bash

# Path to your virtual environment
VENV_PATH="/home/hp/drf-proj/task_manager/env"

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Check if the virtual environment was activated successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment at $VENV_PATH"
    exit 1
fi

# Start Celery worker in the background
echo "Starting Celery worker..."
celery -A task_manager worker -l info --logfile=celery_worker.log &

# Check if Celery worker started successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Celery worker"
    exit 1
fi

# Start Celery Beat in the background
# echo "Starting Celery Beat..."
# celery -A task_manager beat -l info --logfile=celery_beat.log &

# Check if Celery Beat started successfully
# if [ $? -ne 0 ]; then
#     echo "Error: Failed to start Celery Beat"
#     exit 1
# fi

# Start Uvicorn server in the foreground
echo "Starting Uvicorn server..."
uvicorn task_manager.asgi:app --host 127.0.0.1 --port 8000

# Check if Uvicorn started successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Uvicorn server"
    exit 1
fi