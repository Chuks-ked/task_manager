print("FastAPI app loaded by Django")  # Debug

print("Starting fastapi_app.py")
from fastapi import FastAPI, HTTPException
from asgiref.sync import sync_to_async
from core.models import Task

print("Creating FastAPI app")
app = FastAPI()

@app.get("/tasks/{task_id}")
async def get_public_task(task_id: int):
    print(f"Received request for task_id: {task_id}")
    try:
        task = await sync_to_async(Task.objects.get)(id=task_id)
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "deadline": task.deadline,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")

@app.get("/test/")
async def test_endpoint():
    return {"message": "FastAPI is working"}

print("FastAPI app setup completed")