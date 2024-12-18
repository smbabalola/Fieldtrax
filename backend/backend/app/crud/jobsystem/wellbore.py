# File: backend/app/crud/jobsystem/crud_wellbore.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.wellbore import Wellbore
from app.models.jobsystem.trajectory import Trajectory
from app.models.jobsystem.daily_report import DailyReport
from app.models.jobsystem.physical_barrier import PhysicalBarrier
from app.models.jobsystem.fluid import Fluid
from app.schemas.jobsystem.wellbore import WellboreCreate, WellboreUpdate

class CRUDWellbore(CRUDBase[Wellbore, WellboreCreate, WellboreUpdate]):
    async def get_by_well(
        self,
        db: Session,
        *,
        well_id: str
    ) -> List[Wellbore]:
        """Get all wellbores for a well"""
        return db.query(Wellbore).filter(
            Wellbore.well_id == well_id
        ).order_by(Wellbore.wellbore_number).all()

    async def get_by_name(
        self,
        db: Session,
        *,
        wellbore_name: str
    ) -> Optional[Wellbore]:
        """Get wellbore by name"""
        return db.query(Wellbore).filter(
            Wellbore.wellbore_name == wellbore_name
        ).first()

    async def get_by_number(
        self,
        db: Session,
        *,
        wellbore_number: str
    ) -> Optional[Wellbore]:
        """Get wellbore by number"""
        return db.query(Wellbore).filter(
            Wellbore.wellbore_number == wellbore_number
        ).first()

    async def get_active_wellbores(
        self,
        db: Session
    ) -> List[Wellbore]:
        """Get all active wellbores (with end_date = None)"""
        return db.query(Wellbore).filter(
            Wellbore.end_date.is_(None)
        ).all()

    async def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime
    ) -> List[Wellbore]:
        """Get wellbores by start date range"""
        return db.query(Wellbore).filter(
            Wellbore.start_date >= start_date,
            Wellbore.start_date <= end_date
        ).order_by(Wellbore.start_date).all()

    async def get_planned_wellbores(
        self,
        db: Session
    ) -> List[Wellbore]:
        """Get wellbores with planned dates but not started"""
        return db.query(Wellbore).filter(
            Wellbore.planned_start_date.isnot(None),
            Wellbore.start_date.is_(None)
        ).order_by(Wellbore.planned_start_date).all()

    async def get_completed_wellbores(
        self,
        db: Session
    ) -> List[Wellbore]:
        """Get completed wellbores (with end_date)"""
        return db.query(Wellbore).filter(
            Wellbore.end_date.isnot(None)
        ).order_by(Wellbore.end_date.desc()).all()

    async def calculate_costs(
        self,
        db: Session,
        *,
        wellbore_id: str
    ) -> Optional[dict]:
        """Calculate actual vs planned costs"""
        wellbore = await self.get(db=db, id=wellbore_id)
        if not wellbore:
            return None

        return {
            "planned_cost": wellbore.Planned_well_cost,
            "actual_cost": wellbore.actual_well_cost,
            "variance": (wellbore.actual_well_cost or 0) - (wellbore.Planned_well_cost or 0),
            "variance_percentage": (
                ((wellbore.actual_well_cost or 0) - (wellbore.Planned_well_cost or 0)) 
                / (wellbore.Planned_well_cost or 1)
                * 100 if wellbore.Planned_well_cost else None
            )
        }

    async def get_wellbore_summary(
        self,
        db: Session,
        *,
        wellbore_id: str
    ) -> Optional[dict]:
        """Get comprehensive wellbore summary including related data"""
        wellbore = await self.get(db=db, id=wellbore_id)
        if not wellbore:
            return None

        # Count related records
        daily_reports_count = db.query(DailyReport).filter(
            DailyReport.wellbore_id == wellbore_id
        ).count()
        
        fluids_count = db.query(Fluid).filter(
            Fluid.wellbore_id == wellbore_id
        ).count()
        
        barriers_count = db.query(PhysicalBarrier).filter(
            PhysicalBarrier.wellbore_id == wellbore_id
        ).count()

        # Get latest trajectory point
        latest_trajectory = db.query(Trajectory).filter(
            Trajectory.wellbore_id == wellbore_id
        ).order_by(Trajectory.measured_depth.desc()).first()

        return {
            "wellbore_info": {
                "name": wellbore.wellbore_name,
                "number": wellbore.wellbore_number,
                "status": "Active" if not wellbore.end_date else "Completed",
                "duration": (wellbore.end_date - wellbore.start_date).days if wellbore.end_date and wellbore.start_date else None
            },
            "reports": {
                "daily_reports": daily_reports_count,
                "fluids": fluids_count,
                "barriers": barriers_count
            },
            "trajectory": {
                "max_depth": latest_trajectory.measured_depth if latest_trajectory else None,
                "final_inclination": latest_trajectory.inclination if latest_trajectory else None,
                "final_azimuth": latest_trajectory.azimuth if latest_trajectory else None
            },
            "costs": await self.calculate_costs(db=db, wellbore_id=wellbore_id)
        }

crud_wellbore = CRUDWellbore(Wellbore)

# from app.models.jobsystem.wellbore import Wellbore
# from app.crud.base import CRUDBase

# crud_wellbore = CRUDBase(Wellbore)