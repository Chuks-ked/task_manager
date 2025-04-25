# Task Management Platform
A web-based platform for task creation, assignment, and tracking with AI-driven features.

## Setup
- Django, DRF, FastAPI, PostgreSQL, Celery, Redis
- Database: PostgreSQL (`task_db`) via pgAdmin 4
- Run `uvicorn task_manager.asgi:app --host 127.0.0.1 --port 8000` to start
- Run Celery: `celery -A task_manager worker --loglevel=info`

## Environment Variables
- This project uses a `.env` file to manage sensitive information like:
  - `SECRET_KEY`
  - `DEBUG`
  - `DB_NAME`
  - `DB_USER`
  - `DB_PASSWORD`
  - `EMAIL_HOST_PASSWORD`
- Make sure you create a `.env` file in the root directory with the necessary variables.
- **Important:** `.env` is already listed in `.gitignore`, so it won't be committed to Git.


## Static Files
- Run `python manage.py collectstatic` to gather all static files into the `staticfiles/` folder at the root directory.
- Make sure `staticfiles/` is listed in `.gitignore` to avoid committing collected assets, **unless in production**.


## Features
- User signup/login with JWT authentication
- Task CRUD operations
- Public task view (no login required)
- Async notifications on task updates (via Celery)
- APIs: 
  - `/api/signup/`
  - `/api/token/`
  - `/api/profile/`
  - `/api/tasks/`
  - `/api/tasks/<id>/`
  - `/api/public/tasks/<id>/`
