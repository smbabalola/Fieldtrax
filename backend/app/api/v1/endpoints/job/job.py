# File: backend/app/api/api_v1/endpoints/job/job.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.job import crud_job
from app.schemas.jobsystem.job import JobResponse, JobCreate, JobUpdate, JobView
from app.core.deps import get_db

router = APIRouter()

@router.post("/", response_model=JobResponse)
async def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db)
):
    """Create new job"""
    return await crud_job.create(db=db, obj_in=job_in)

@router.get("/", response_model=List[JobView])
async def read_jobs(
    skip: int = 0,
    limit: int = 100,
    sort_field: str = "created_at",
    sort_order: str = "desc",
    status: str = None,
    search_term: str = None,
    db: Session = Depends(get_db)
):
    """Get all jobs with optional filters"""
    filters = {
        "sort_field": sort_field,
        "sort_order": sort_order,
        "status": status,
        "search_term": search_term
    }
    jobs = await crud_job.get_multi(db, skip=skip, limit=limit, filters=filters)
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")
    return jobs

@router.get("/active", response_model=List[JobResponse])
async def read_active_jobs(
    db: Session = Depends(get_db)
):
    """Get active jobs"""
    return await crud_job.get_active_jobs(db=db)

@router.get("/{job_id}", response_model=JobView)
async def read_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Get job by ID"""
    job = await crud_job.get(db=db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_in: JobUpdate,
    db: Session = Depends(get_db)
):
    """Update job"""
    job = await crud_job.get(db=db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return await crud_job.update(db=db, db_obj=job, obj_in=job_in)