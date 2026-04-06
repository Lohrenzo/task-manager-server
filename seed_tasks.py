from datetime import datetime
from app.db.database import db, TaskModel, init_db
from app.schemas.task import TaskStatus

# Make sure tables exist
init_db()

# Seed data from frontend
seed_tasks = [
    {
        "id": "task-1",
        "title": "Review case bundle for Smith v. Crown",
        "description": "Check all exhibits are paginated correctly and that the index matches the physical bundle submitted on 21 March.",
        "status": TaskStatus.TODO,
        "dueDate": "2026-04-10",
        "dueTime": "09:00",
        "assignee": "J. Harrison",
        "caseRef": "CR-2026-0412",
        "created_at": datetime.fromisoformat("2026-04-01T08:00:00+00:00"),
        "updated_at": datetime.fromisoformat("2026-04-01T08:00:00+00:00"),
    },
    {
        "id": "task-2",
        "title": "Issue hearing notice to all parties",
        "description": "Send the confirmed hearing date of 28 April to claimant solicitors and the defendant directly.",
        "status": TaskStatus.TODO,
        "dueDate": "2026-04-08",
        "dueTime": "12:00",
        "assignee": "P. Okafor",
        "caseRef": "CV-2025-8871",
        "created_at": datetime.fromisoformat("2026-04-02T09:15:00+00:00"),
        "updated_at": datetime.fromisoformat("2026-04-02T09:15:00+00:00"),
    },
    {
        "id": "task-3",
        "title": "Prepare court order for sealing",
        "description": "Draft the consent order following settlement. Obtain judge signature before 5 pm.",
        "status": TaskStatus.IN_PROGRESS,
        "dueDate": "2026-04-07",
        "dueTime": "17:00",
        "assignee": "J. Harrison",
        "caseRef": "FA-2026-0033",
        "created_at": datetime.fromisoformat("2026-04-03T10:30:00+00:00"),
        "updated_at": datetime.fromisoformat("2026-04-05T14:20:00+00:00"),
    },
    {
        "id": "task-4",
        "title": "Allocate interpreter for upcoming hearing",
        "description": "Contact the interpreter agency for a Punjabi interpreter for the 14 April hearing.",
        "status": TaskStatus.IN_PROGRESS,
        "dueDate": "2026-04-09",
        "dueTime": "10:00",
        "assignee": "S. Begum",
        "caseRef": "IA-2026-1102",
        "created_at": datetime.fromisoformat("2026-04-04T11:00:00+00:00"),
        "updated_at": datetime.fromisoformat("2026-04-06T08:45:00+00:00"),
    },
    {
        "id": "task-5",
        "title": "Archive closed probate file",
        "description": "File has been concluded. Scan all originals, update the case management system, and send to records.",
        "status": TaskStatus.DONE,
        "dueDate": "2026-04-05",
        "dueTime": "16:30",
        "assignee": "P. Okafor",
        "caseRef": "PB-2025-4490",
        "created_at": datetime.fromisoformat("2026-03-28T09:00:00+00:00"),
        "updated_at": datetime.fromisoformat("2026-04-05T16:25:00+00:00"),
    },
    {
        "id": "task-6",
        "title": "Confirm witness availability",
        "description": "Call all three witnesses to confirm attendance on 22 April. Log responses in CMS.",
        "status": TaskStatus.DONE,
        "dueDate": "2026-04-04",
        "dueTime": "15:00",
        "assignee": "S. Begum",
        "caseRef": "CR-2026-0215",
        "created_at": datetime.fromisoformat("2026-03-30T13:30:00+00:00"),
        "updated_at": datetime.fromisoformat("2026-04-04T14:50:00+00:00"),
    },
]

# Seed into DB
for task_data in seed_tasks:
    db.insert(task_data)

print("✅ Seeded frontend tasks into the database!")
