import os
import django
from fastapi import  FastAPI, HTTPException
from django.conf import settings
from core.models import Task

# to set up django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

app = FastAPI()

@app.get("/public/tasks/{task_id}")
async def get_public_task(task_id:int):
    try:
        task = Task.objects.get(id=task_id)
        return { 
            "id":task.id,
            "title":task.title,
            "description":task.description,
            "status":task.status,
            "deadline":task.deadline,
            "created_at":task.created_at,
            "updated_at":task.updated_at,
        }
    except Task.DoesNotExist:
        return HTTPException(status_code=404, detail="Task not found")