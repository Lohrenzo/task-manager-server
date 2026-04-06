from __future__ import annotations
import uuid
from datetime import date, datetime, timezone
from typing import Optional
from fastapi import Query, APIRouter, HTTPException, status
from app.db.database import TaskModel, db
from app.schemas.task import (
    MessageResponse,
    TaskCreate,
    TaskInDB,
    TaskStatus,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter()


def _get_or_404(task_id: str) -> TaskInDB:
    task = db.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' was not found.",
        )
    return task


def _to_response(task: TaskModel) -> TaskResponse:
    """
    Convert a SQLAlchemy TaskModel instance to a TaskResponse Pydantic model.
    Handles snake_case → camelCase mapping.
    """
    data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "dueDate": task.dueDate,
        "dueTime": task.dueTime,
        "assignee": task.assignee,
        "caseRef": task.caseRef,
        "createdAt": task.created_at,
        "updatedAt": task.updated_at,
    }

    return TaskResponse(**data)


@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)

    task_data = {
        "id": str(uuid.uuid4()),
        "created_at": now,
        "updated_at": now,
        **payload.model_dump(),
    }

    task = db.insert(task_data)
    return _to_response(task)


@router.get("/tasks", response_model=TaskListResponse)
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    status: Optional[TaskStatus] = None,
    assignee: Optional[str] = None,
    dueDate: Optional[date] = None,
) -> TaskListResponse:
    tasks = db.get_all(
        skip=skip,
        limit=limit,
        status=status,
        assignee=assignee,
        dueDate=dueDate,
    )

    total = db.count()

    return TaskListResponse(
        total=total,
        tasks=[_to_response(t) for t in tasks],
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str) -> TaskResponse:
    task = _get_or_404(task_id)
    return _to_response(task)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    _get_or_404(task_id)

    updates = payload.model_dump(exclude_none=True)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Request body must contain at least one field to update.",
        )

    updated = db.update(task_id, updates)
    return _to_response(updated)


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(task_id: str) -> MessageResponse:
    _get_or_404(task_id)
    db.delete(task_id)
    return MessageResponse(message=f"Task '{task_id}' deleted successfully.")
