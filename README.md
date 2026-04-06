# Task Manager Server

A lightweight and production-ready Task Management API built with **FastAPI**, **SQLAlchemy**, and **SQLite/PostgreSQL**.  
It provides CRUD operations for managing tasks, along with filtering, validation, and rate limiting.

---

## 🚀 Features

- Create, read, update, and delete tasks
- Filter tasks by status, assignee, and due date
- Input validation using Pydantic (v2)
- SQLAlchemy ORM with clean database abstraction
- RESTful API design
- Global rate limiting (Upstash Redis ready)
- Fully tested with pytest
- Modern FastAPI lifespan events (no deprecated patterns)

---

## 🧱 Tech Stack

- **FastAPI** – high-performance API framework
- **SQLAlchemy** – ORM for database interactions
- **Pydantic v2** – data validation and serialization
- **SQLite / PostgreSQL** – database options
- **Pytest** – testing framework
- **Upstash Redis** – rate limiting (production-ready)

---

## 📁 Project Structure

```
app/
├── db/              # Database setup and ORM models
├── routers/         # API route definitions
├── schemas/         # Pydantic schemas (validation)
├── middleware/      # Rate limiting middleware
├── main.py          # App entry point
tests/               # Unit and integration tests
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Lohrenzo/task-manager-server.git
cd task-manager-server
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./test.db

# Optional (for rate limiting)
UPSTASH_REDIS_REST_URL=your_url
UPSTASH_REDIS_REST_TOKEN=your_token
```

---

## ▶️ Running the API

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://localhost:8000/api/v1/
```

Interactive docs:

```
http://localhost:8000/docs
```

---

## 📌 API Endpoints

| Method | Endpoint           | Description    |
| ------ | ------------------ | -------------- |
| GET    | /api/v1/tasks      | List all tasks |
| GET    | /api/v1/tasks/{id} | Get task by ID |
| POST   | /api/v1/tasks      | Create a task  |
| PATCH  | /api/v1/tasks/{id} | Update a task  |
| DELETE | /api/v1/tasks/{id} | Delete a task  |

---

## 🧪 Running Tests

```bash
pytest tests/test_tasks.py
```

Optional with coverage:

```bash
pytest --cov=app
```

---

## 🛡️ Rate Limiting

- Implemented using **Upstash Redis**
- Applied globally via FastAPI middleware
- Protects API from excessive requests (e.g. 60 req/min per IP)

---

## 📌 Notes

- Uses ISO format for dates (`YYYY-MM-DD`) and time (`HH:MM`)
- Designed to be easily extendable (authentication, roles, etc.)
- Ready for deployment with minimal changes

---

## 📈 Future Improvements

- Authentication (JWT / OAuth)
- Role-based access control
- Pagination metadata enhancements
- Docker support
- CI/CD pipeline

---

## 📄 License

This project is open-source and available under the MIT License.
