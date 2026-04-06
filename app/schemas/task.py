from __future__ import annotations
from datetime import datetime, date, time
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    dueDate: Optional[date] = None
    dueTime: Optional[str] = None  # "HH:MM"
    assignee: Optional[str] = None
    caseRef: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be blank")
        return v.strip()

    @field_validator("dueTime")
    @classmethod
    def validate_due_time(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            time.fromisoformat(v)
        except ValueError:
            raise ValueError("dueTime must be in HH:MM format")
        return v


class TaskInDB(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(use_enum_values=True)


class TaskCreate(TaskBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Review bail application",
                "description": "Assess case",
                "status": "todo",
                "dueDate": "2025-06-15",
                "dueTime": "10:00",
                "assignee": "John Doe",
                "caseRef": "CR-2024-0042",
            }
        }
    )


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    dueDate: Optional[date] = None
    dueTime: Optional[str] = None
    assignee: Optional[str] = None
    caseRef: Optional[str] = None

    # Validator
    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("title must not be blank")
        return v.strip() if v else v


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    dueDate: Optional[date]
    dueTime: Optional[str]
    assignee: Optional[str]
    caseRef: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    total: int
    tasks: List[TaskResponse]


class MessageResponse(BaseModel):
    message: str
