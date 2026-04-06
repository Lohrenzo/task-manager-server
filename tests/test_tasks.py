# tests/test_tasks.py
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import db
from app.schemas.task import TaskStatus
from datetime import date

client = TestClient(app)


# ── Fixtures ─────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def clear_db():
    """Clear the database before and after each test"""
    db.delete_all()
    yield
    db.delete_all()


@pytest.fixture
def task_payload():
    return {
        "title": "Review evidence bundle",
        "description": "Check all exhibits listed in the prosecution schedule.",
        "status": "todo",
        "dueDate": str(date.today()),
        "dueTime": "09:00",
        "assignee": "John Doe",
        "caseRef": "CR-2024-0042",
    }


@pytest.fixture
def create_task(task_payload):
    def _create(payload=None):
        response = client.post("/api/v1/tasks", json=payload or task_payload)
        assert response.status_code == 201
        return response.json()

    return _create


# ── Test Create Task ───────────────────────────────────────────────────────
class TestCreateTask:

    def test_create_task_success(self, create_task, task_payload):
        data = create_task()
        assert data["title"] == task_payload["title"]
        assert data["status"] == task_payload["status"]
        assert "id" in data
        assert "createdAt" in data
        assert "updatedAt" in data

    def test_create_task_without_optional_fields(self, create_task, task_payload):
        payload = {**task_payload}
        payload.pop("description")
        payload.pop("assignee")
        data = create_task(payload)
        assert data["description"] is None
        assert data["assignee"] is None

    @pytest.mark.parametrize("invalid_title", ["", "   "])
    def test_create_task_invalid_title(self, invalid_title, task_payload):
        payload = {**task_payload, "title": invalid_title}
        response = client.post("/api/v1/tasks", json=payload)
        assert response.status_code == 422

    def test_create_task_invalid_status(self, task_payload):
        payload = {**task_payload, "status": "invalid"}
        response = client.post("/api/v1/tasks", json=payload)
        assert response.status_code == 422


# ── Test List Tasks ───────────────────────────────────────────────────────
class TestListTasks:

    def test_list_tasks_empty(self):
        response = client.get("/api/v1/tasks")
        data = response.json()
        assert response.status_code == 200
        assert data["total"] == 0
        assert data["tasks"] == []

    def test_list_tasks_multiple(self, create_task):
        t1 = create_task()
        t2 = create_task(
            {"title": "Second Task", "status": "todo", "dueDate": str(date.today())}
        )
        response = client.get("/api/v1/tasks")
        data = response.json()
        assert data["total"] == 2
        ids = [t["id"] for t in data["tasks"]]
        # Newest first
        assert ids[0] == t2["id"]
        assert ids[1] == t1["id"]


# ── Test Get Task ─────────────────────────────────────────────────────────
class TestGetTask:

    def test_get_task_success(self, create_task):
        task = create_task()
        response = client.get(f"/api/v1/tasks/{task['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task["id"]

    def test_get_task_not_found(self):
        response = client.get("/api/v1/tasks/nonexistent-id")
        assert response.status_code == 404


# ── Test Update Task ──────────────────────────────────────────────────────
class TestUpdateTask:

    def test_update_task_title(self, create_task):
        task = create_task()
        response = client.patch(
            f"/api/v1/tasks/{task['id']}", json={"title": "Updated"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

    def test_update_task_not_found(self):
        response = client.patch("/api/v1/tasks/ghost-id", json={"title": "X"})
        assert response.status_code == 404

    def test_update_task_empty_body_returns_422(self, create_task):
        task = create_task()
        response = client.patch(f"/api/v1/tasks/{task['id']}", json={})
        assert response.status_code == 422


# ── Test Update Task Status ───────────────────────────────────────────────
class TestUpdateTaskStatus:

    @pytest.mark.parametrize("status", ["todo", "in-progress", "done"])
    def test_update_status_success(self, create_task, status):
        task = create_task()
        response = client.patch(f"/api/v1/tasks/{task['id']}", json={"status": status})
        assert response.status_code == 200
        assert response.json()["status"] == status

    def test_update_status_invalid(self, create_task):
        task = create_task()
        response = client.patch(
            f"/api/v1/tasks/{task['id']}", json={"status": "invalid"}
        )
        assert response.status_code == 422

    def test_update_status_not_found(self):
        response = client.patch("/api/v1/tasks/ghost-id", json={"status": "done"})
        assert response.status_code == 404


# ── Test Delete Task ──────────────────────────────────────────────────────
class TestDeleteTask:

    def test_delete_task_success(self, create_task):
        task = create_task()
        response = client.delete(f"/api/v1/tasks/{task['id']}")
        assert response.status_code == 200
        assert client.get(f"/api/v1/tasks/{task['id']}").status_code == 404

    def test_delete_task_not_found(self):
        response = client.delete("/api/v1/tasks/nonexistent-id")
        assert response.status_code == 404


# ── Test Root Endpoint ─────────────────────────────────────────────────
class TestRoot:

    def test_root_ok(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
