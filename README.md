# 🚀 Task Management Platform

A web-based platform for task creation, assignment, and tracking with AI-driven features.

---

## 📚 Tech Stack
- **Backend:** Django, Django Rest Framework (DRF), FastAPI
- **Database:** PostgreSQL
- **Async Tasks:** Celery + Redis
- **Authentication:** JWT
- **Environment Management:** python-decouple

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Chuks-ked/task_manager.git
cd task_manager
```

### 2. Create and configure `.env` file
This project uses a `.env` file for managing sensitive information.  
Create a `.env` file in your root directory:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
EMAIL_HOST_PASSWORD=your_email_password
```

> **Note:** `.env` is already included in `.gitignore` and won't be tracked by Git.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the database
- Create a PostgreSQL database named `task_db` using pgAdmin or CLI.
- Make sure the credentials match those in your `.env` file.

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```
- Collected files will appear in the `staticfiles/` folder.
- Make sure `staticfiles/` is listed in `.gitignore` to avoid committing them, **unless in production**.

### 7. Start the servers
- **Run FastAPI server:**
  ```bash
  uvicorn task_manager.asgi:app --host 127.0.0.1 --port 8000
  ```
- **Run Celery worker:**
  ```bash
  celery -A task_manager worker --loglevel=info
  ```

---

## 🚪 API Endpoints

### 🔐 Authentication
- `POST /api/signup/` – Create a new user
- `POST /api/token/` – Get JWT tokens

### 👤 User Profile
- `GET /api/profile/` – Retrieve logged-in user profile

### ✅ Tasks
- `GET /api/tasks/` – List user tasks
- `POST /api/tasks/` – Create new task
- `GET /api/tasks/<id>/` – Retrieve, update, or delete a task

### 🌍 Public Tasks
- `GET /api/public/tasks/<id>/` – View a public task without login

---

## 🛡️ Security
- All credentials and sensitive configurations are managed with environment variables using `python-decouple`.
- JWT is used for secure authentication.
- Static and media files are handled properly with `collectstatic`.

---

## 🤝 How to Contribute
1. Fork this repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes.
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Open a Pull Request.

---

## 🧠 Author
Built and maintained by **Jeremiah**
