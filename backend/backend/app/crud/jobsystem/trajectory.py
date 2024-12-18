# File: backend/app/crud/jobsystem/crud_trajectory.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.trajectory import Trajectory
from app.schemas.jobsystem.trajectory import TrajectoryCreate, TrajectoryUpdate

class CRUDTrajectory(CRUDBase[Trajectory, TrajectoryCreate, TrajectoryUpdate]):
    async def get_by_wellbore(
        self,
        db: Session,
        *,
        wellbore_id: str
    ) -> List[Trajectory]:
        """Get all trajectory points for a wellbore"""
        return db.query(Trajectory).filter(
            Trajectory.wellbore_id == wellbore_id
        ).order_by(Trajectory.measured_depth).all()

    async def get_by_depth_range(
        self,
        db: Session,
        *,
        wellbore_id: str,
        min_depth: float,
        max_depth: float
    ) -> List[Trajectory]:
        """Get trajectory points within depth range"""
        return db.query(Trajectory).filter(
            Trajectory.wellbore_id == wellbore_id,
            Trajectory.measured_depth >= min_depth,
            Trajectory.measured_depth <= max_depth
        ).order_by(Trajectory.measured_depth).all()
        
crud_trajectory = CRUDTrajectory(Trajectory)

# from app.models.jobsystem.trajectory import Trajectory
# from app.crud.base import CRUDBase

# crud_trajectory = CRUDBase(Trajectory)