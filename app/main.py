from app.middleware.rate_limit import RateLimitMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import tasks
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()  # initialize database tables
    print("Startup complete")
    yield
    # Shutdown code
    print("Shutdown complete")


app = FastAPI(
    title="HMCTS Task Management Backend API",
    description=(
        "A RESTful API enabling HMCTS caseworkers to create, retrieve, "
        "update, and delete tasks efficiently."
    ),
    version="1.0.0",
    contact={"name": "Laurence"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://task-manager-client-woad.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)


app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"])


@app.get("/", tags=["Root"])
async def root():
    return {"status": "healthy", "message": "HMCTS Task Management API is running."}
