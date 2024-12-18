# backend/tests/test_jobs.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from uuid import uuid4

from app.core.units.quantity import Depth, Volume, Pressure
from app.models.job.models import Job, JobCreate, DailyReport

@pytest.fixture
def test_db_session():
    # Setup test database
    from app.db.session import SessionLocal
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def sample_job_data():
    return {
        "jobid": "TEST-001",
        "jobcenter_id": 1,
        "well_name": "TEST-WELL-01",
        "rigid": "RIG-001",
        "country": "US",
        "field": "TEST FIELD",
        "contractor": "Test Contractor",
        "contractorrep": "John Doe",
        "waterdepth": {"value": 1000, "unit": "ft"},
        "spuddate": datetime.utcnow().isoformat()
    }

class TestJobModel:
    def test_create_job(self, test_db_session, sample_job_data):
        job = Job(**sample_job_data)
        test_db_session.add(job)
        test_db_session.commit()
        
        assert job.id is not None
        assert job.well_name == sample_job_data["well_name"]
        assert isinstance(job.waterdepth, Depth)
        assert job.waterdepth.value == 1000

    def test_update_job(self, test_db_session, sample_job_data):
        job = Job(**sample_job_data)
        test_db_session.add(job)
        test_db_session.commit()

        job.well_name = "UPDATED-WELL"
        test_db_session.commit()
        
        updated_job = test_db_session.query(Job).filter_by(id=job.id).first()
        assert updated_job.well_name == "UPDATED-WELL"

class TestJobCRUD:
    def test_daily_report_creation(self, test_db_session, sample_job_data):
        from ..app.crud.job import job as job_crud
        
        # Create job first
        job = job_crud.create(test_db_session, obj_in=sample_job_data)
        
        # Create daily report
        report_data = {
            "report_date": datetime.now(),
            "operations": ["Test operation"],
            "summary": "Test summary"
        }
        report = job_crud.create_daily_report(
            test_db_session,
            job_id=job.id,
            report=report_data
        )
        
        assert report.job_id == job.id
        assert report.summary == "Test summary"

    def test_fluid_management(self, test_db_session, sample_job_data):
        from app.crud.job import job as job_crud
        
        job = job_crud.create(test_db_session, obj_in=sample_job_data)
        
        fluid_data = {
            "fluid_type": "Mud",
            "volume": {"value": 500, "unit": "bbl"},
            "density": {"value": 12.5, "unit": "ppg"},
            "description": "Test fluid"
        }
        
        fluid = job_crud.add_fluid(
            test_db_session,
            job_id=job.id,
            fluid=fluid_data
        )
        
        assert fluid.job_id == job.id
        assert isinstance(fluid.volume, Volume)
        assert fluid.volume.value == 500

class TestValidation:
    def test_water_depth_validation(self, test_db_session):
        from app.core.validators import EnhancedJobValidation
        
        invalid_data = {
            "waterdepth": {"value": -100, "unit": "ft"}
        }
        
        with pytest.raises(ValueError) as exc_info:
            EnhancedJobValidation(**invalid_data)
        assert "Water depth cannot be negative" in str(exc_info.value)

    def test_spud_date_validation(self, test_db_session):
        from app.core.validators import EnhancedJobValidation
        
        future_date = datetime.utcnow().replace(year=datetime.utcnow().year + 1)
        invalid_data = {
            "spuddate": future_date
        }
        
        with pytest.raises(ValueError) as exc_info:
            EnhancedJobValidation(**invalid_data)
        assert "Spud date cannot be in the future" in str(exc_info.value)

# tests/test_business_rules.py
def test_job_update_permission():
    from app.core.business_rules import JobBusinessRules
    
    # Test supervisor permission
    supervisor = {"role": "supervisor"}
    active_job = {"status": "active"}
    assert JobBusinessRules.can_update_job(active_job, supervisor) == True
    
    # Test completed job
    completed_job = {"status": "completed"}
    assert JobBusinessRules.can_update_job(completed_job, supervisor) == False