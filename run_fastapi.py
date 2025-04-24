import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
import django
django.setup()

import uvicorn
from task_manager.fastapi_app import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)