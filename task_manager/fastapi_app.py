print("Starting fastapi_app.py")
from fastapi import FastAPI, HTTPException
from asgiref.sync import sync_to_async
from django.core.cache import cache
from core.models import Task
from core.serializers import TaskSerializer

app = FastAPI()

@app.get("/test/")
async def test_endpoint():
    return {"message": "FastAPI is working"}

@app.get("/tasks/{task_id}/")
async def get_public_task(task_id: int):
    print(f"Received request for task_id: {task_id}")
    # Check cache first
    cache_key = f'public_task_{task_id}'
    cached_task = cache.get(cache_key)
    print(f"Cached task for {cache_key}: {cached_task}")
    if cached_task is not None:
        return cached_task

    try:
        task = await sync_to_async(Task.objects.select_related('assignee').get)(id=task_id)
        serializer = TaskSerializer(task)
        task_data = serializer.data
        cache.set(cache_key, task_data, timeout=60 * 15)        
        return task_data
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
