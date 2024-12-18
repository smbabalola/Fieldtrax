# File: backend/app/api/v1/endpoints/wellbore/trajectory.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.trajectory import crud_trajectory
from app.schemas.jobsystem.trajectory import TrajectoryResponse as Trajectory, TrajectoryCreate, TrajectoryUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Trajectory)
async def create_trajectory(
    *,
    db: Session = Depends(get_db),
    trajectory_in: TrajectoryCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new trajectory point"""
    return await crud_trajectory.create(db=db, obj_in=trajectory_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[Trajectory])
async def get_trajectory_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all trajectory points for a wellbore"""
    return await crud_trajectory.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/wellbore/{wellbore_id}/depth-range", response_model=List[Trajectory])
async def get_trajectory_by_depth(
    wellbore_id: str,
    min_depth: float,
    max_depth: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get trajectory points within depth range"""
    return await crud_trajectory.get_by_depth_range(
        db=db,
        wellbore_id=wellbore_id,
        min_depth=min_depth,
        max_depth=max_depth
    )

@router.put("/{trajectory_id}", response_model=Trajectory)
async def update_trajectory(
    *,
    db: Session = Depends(get_db),
    trajectory_id: str,
    trajectory_in: TrajectoryUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update trajectory point"""
    trajectory = await crud_trajectory.get(db=db, id=trajectory_id)
    if not trajectory:
        raise HTTPException(status_code=404, detail="Trajectory point not found")
    return await crud_trajectory.update(db=db, db_obj=trajectory, obj_in=trajectory_in)