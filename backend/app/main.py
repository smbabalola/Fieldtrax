from typing import Optional
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.crud.jobsystem.job import crud_job
from app.database.session import get_db
# ...existing imports...

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/jobs")
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    sort_field: str = "created_at",
    sort_order: str = "desc",
    status: Optional[str] = Query(None),
    search_term: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    filters = {
        "status": status,
        "search_term": search_term,
        "sort_field": sort_field,
        "sort_order": sort_order
    }
    jobs = await crud_job.get_multi(db, skip=skip, limit=limit, filters=filters)
    return jobs

# ...existing code...
