from __future__ import annotations

from datetime import datetime, timezone, date
from typing import List, Optional

from sqlalchemy import create_engine, String, DateTime, Enum, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.future import select

from app.schemas.task import TaskStatus
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
)  # Default to SQLite for testing

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# DB Model
class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus))

    dueDate: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    dueTime: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    assignee: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    caseRef: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Database class
class Database:

    def insert(self, task_data: dict) -> TaskModel:
        """
        Insert a new task into the database.
        Converts dueDate from string to date if necessary.
        """
        with SessionLocal() as session:
            # Ensure dueDate is a Python date object
            if "dueDate" in task_data and task_data["dueDate"] is not None:
                if isinstance(task_data["dueDate"], str):
                    task_data["dueDate"] = date.fromisoformat(task_data["dueDate"])

            task = TaskModel(**task_data)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def update(self, task_id: str, updates: dict) -> Optional[TaskModel]:
        """
        Update an existing task in the database.
        Converts dueDate from string to date if necessary.
        """
        with SessionLocal() as session:
            task = session.get(TaskModel, task_id)
            if not task:
                return None

            # Convert dueDate if needed
            if "dueDate" in updates and updates["dueDate"] is not None:
                if isinstance(updates["dueDate"], str):
                    updates["dueDate"] = date.fromisoformat(updates["dueDate"])

            for key, value in updates.items():
                setattr(task, key, value)

            task.updated_at = datetime.now(timezone.utc)

            session.commit()
            session.refresh(task)
            return task

    def get_by_id(self, task_id: str) -> Optional[TaskModel]:
        with SessionLocal() as session:
            return session.get(TaskModel, task_id)

    def delete(self, task_id: str) -> bool:
        with SessionLocal() as session:
            task = session.get(TaskModel, task_id)
            if not task:
                return False

            session.delete(task)
            session.commit()
            return True

    def delete_all(self):
        with SessionLocal() as session:
            session.query(TaskModel).delete()
            session.commit()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TaskStatus] = None,
        assignee: Optional[str] = None,
        dueDate: Optional[date] = None,
    ) -> List[TaskModel]:

        with SessionLocal() as session:
            query = select(TaskModel)

            # Filters
            if status:
                query = query.where(TaskModel.status == status)

            if assignee:
                query = query.where(TaskModel.assignee == assignee)

            if dueDate:
                query = query.where(TaskModel.dueDate == dueDate)

            # Order + Pagination
            query = query.order_by(TaskModel.created_at.desc())
            query = query.offset(skip).limit(limit)

            result = session.execute(query)
            return result.scalars().all()

    def count(self) -> int:
        with SessionLocal() as session:
            return session.query(TaskModel).count()


db = Database()
