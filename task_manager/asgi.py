import os
import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

# Import FastAPI app after Django setup
from task_manager.fastapi_app import app as fastapi_app

# Get Django ASGI application
django_app = get_asgi_application()

# Create a FastAPI app to mount both Django and FastAPI
app = FastAPI()

# Mount static files at /static
app.mount("/static", StaticFiles(directory="staticfiles"), name="static")

# Mount FastAPI at /api/public/
app.mount("/api/public", fastapi_app)

# Mount Django at the root (/)
app.mount("/", django_app)

# Optional: Add a test route at the root
@app.get("/")
async def root():
    return {"message": "Root endpoint - Django and FastAPI are running"}
