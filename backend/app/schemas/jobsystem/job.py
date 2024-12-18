#job
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.jobsystem.job_center import JobCenterBase, JobCenterResponse
from app.schemas.jobsystem.job_log import JobLogBase, JobLogResponse
from app.schemas.jobsystem.time_sheet import TimeSheetBase, TimeSheetResponse
from app.schemas.jobsystem.well import WellBase, WellResponse
from app.schemas.rigsystem.rig import RigBase, RigResponse
from app.schemas.jobsystem.operator import OperatorBase, OperatorResponse
from app.schemas.logisticsystem.purchase_order import PurchaseOrderBase, PurchaseOrderResponse

class JobBase(BaseModel):
    jobcenter_id: str
    job_name: str
    job_description: Optional[str]
    rig_id: str
    purchase_order_id: str
    operator_id: str
    well_id: str
    service_code: Optional[str]
    country: Optional[str]
    measured_depth: Optional[float]
    total_vertical_depth: Optional[float]
    spud_date: Optional[datetime]
    status: Optional[str]
    mobilization_date: Optional[datetime]
    demobilization_date: Optional[datetime]
    job_closed: Optional[bool]
    trainingfile: Optional[bool]
    
class JobCreate(JobBase):
    jobcenter_id: str
    job_name: str
    job_description: Optional[str]
    rig_id: str
    purchase_order_id: str
    operator_id: str
    well_id: str
    service_code: Optional[str]
    country: Optional[str]
    measured_depth: Optional[float]
    total_vertical_depth: Optional[float]
    spud_date: Optional[datetime]
    status: Optional[str]
    mobilization_date: Optional[datetime]
    demobilization_date: Optional[datetime]
    job_closed: Optional[bool]
    trainingfile: Optional[bool]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class JobUpdate(JobBase):
    pass

class JobResponse(JobBase):
    id: Optional[str] = None

    class Config:
        from_attributes = True

class JobView(JobBase):
    id: Optional[str] = None
    job_center: JobCenterResponse
    well: WellResponse 
    job_logs: List[JobLogResponse] = []
    time_sheets: List[TimeSheetResponse] = []
    rig: RigResponse
    operator: OperatorResponse 
    purchase_order: PurchaseOrderResponse 
