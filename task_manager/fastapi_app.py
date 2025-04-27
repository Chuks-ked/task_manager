print("Starting fastapi_app.py")
from fastapi import FastAPI, HTTPException, Request
from asgiref.sync import sync_to_async
from django.core.cache import cache
from core.models import Task
from core.serializers import TaskSerializer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()

# Initialize rate limiter with Redis backend
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379/2"
)

# Set the limiter on the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/test/")
async def test_endpoint():
    return {"message": "FastAPI is working"}

@app.get("/tasks/{task_id}/")
@limiter.limit("100/day")
async def get_public_task(task_id: int, request: Request):
#     print(f"Received request for task_id: {task_id}")
#     # Check cache first
    cache_key = f'public_task_{task_id}'
    cached_task = cache.get(cache_key)
#     print(f"Cached task for {cache_key}: {cached_task}")
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
    
@app.get("/task/{task_id}/status/")
@limiter.limit("100/day")
async def get_task_status(task_id: int, request: Request):
    cache_key = f'task_status_{task_id}'
    cached_status = cache.get(cache_key)
    if cached_status is not None:
        return {"status": cached_status}

    try:
        task = await sync_to_async(Task.objects.get)(id=task_id)
        status = task.status
        cache.set(cache_key, status, timeout=60 * 15)
        return {"status": status}
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
