# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.core.config import settings
from fastapi.testclient import TestClient
from backend.app.db.session import get_db
from main import app

@pytest.fixture(scope="session")
def test_db():
    # Use SQLite in-memory database for testing
    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create test database
    Base.metadata.create_all(bind=engine)
    
    yield TestingSessionLocal()
    
    # Drop test database
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

# tests/test_auth.py
import pytest
from app.core.security import create_access_token
from app.models.user import User

def test_login_success(test_client, test_db):
    # Create test user
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$test_hash"
    )
    test_db.add(user)
    test_db.commit()
    
    response = test_client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(test_client):
    response = test_client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401

def test_password_reset_request(test_client, test_db):
    response = test_client.post(
        "/api/auth/password-reset",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200

# tests/test_jobs.py
from app.models.job.models import Job, DailyReport
from datetime import datetime

def test_create_job(test_client, test_db):
    job_data = {
        "well_name": "Test Well",
        "field": "Test Field",
        "country": "Test Country",
        "spuddate": datetime.utcnow().isoformat()
    }
    
    response = test_client.post("/api/jobs/", json=job_data)
    assert response.status_code == 201
    assert response.json()["well_name"] == "Test Well"

def test_get_job(test_client, test_db):
    # Create test job
    job = Job(
        well_name="Test Well",
        field="Test Field",
        country="Test Country",
        spuddate=datetime.utcnow()
    )
    test_db.add(job)
    test_db.commit()
    
    response = test_client.get(f"/api/jobs/{job.id}")
    assert response.status_code == 200
    assert response.json()["well_name"] == "Test Well"

def test_update_job(test_client, test_db):
    # Create test job
    job = Job(
        well_name="Test Well",
        field="Test Field",
        country="Test Country",
        spuddate=datetime.utcnow()
    )
    test_db.add(job)
    test_db.commit()
    
    update_data = {"well_name": "Updated Well"}
    response = test_client.patch(f"/api/jobs/{job.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["well_name"] == "Updated Well"

# tests/test_daily_reports.py
def test_create_daily_report(test_client, test_db):
    # Create test job first
    job = Job(
        well_name="Test Well",
        field="Test Field",
        country="Test Country",
        spuddate=datetime.utcnow()
    )
    test_db.add(job)
    test_db.commit()
    
    report_data = {
        "job_id": str(job.id),
        "report_date": datetime.utcnow().isoformat(),
        "operations": ["Test operation"],
        "summary": "Test summary"
    }
    
    response = test_client.post("/api/daily-reports/", json=report_data)
    assert response.status_code == 201
    assert response.json()["summary"] == "Test summary"

def test_get_daily_reports(test_client, test_db):
    # Create test job and report
    job = Job(
        well_name="Test Well",
        field="Test Field",
        country="Test Country",
        spuddate=datetime.utcnow()
    )
    test_db.add(job)
    
    report = DailyReport(
        job_id=job.id,
        report_date=datetime.utcnow(),
        operations=["Test operation"],
        summary="Test summary"
    )
    test_db.add(report)
    test_db.commit()
    
    response = test_client.get(f"/api/jobs/{job.id}/daily-reports")
    assert response.status_code == 200
    assert len(response.json()) > 0

# tests/test_websocket.py
from fastapi.websockets import WebSocket
from app.core.ws.manager import ConnectionManager

async def test_websocket_connection(test_client):
    manager = ConnectionManager()
    
    # Test connection
    websocket = WebSocket()
    await manager.connect(websocket, "test_job_id", "test_user_id")
    assert len(manager.active_connections) == 1
    
    # Test disconnection
    await manager.disconnect(websocket)
    assert len(manager.active_connections) == 0

# tests/test_units.py
from app.core.units.quantity import Depth, Length, Pressure

def test_depth_conversion():
    depth = Depth(100, "ft")
    assert abs(depth.to_unit("m") - 30.48) < 0.01

def test_pressure_calculation():
    depth = Depth(1000, "ft")
    density = 8.6  # ppg
    pressure = depth.calculate_hydrostatic_pressure(density)
    assert abs(pressure.to_unit("psi") - 447.2) < 0.1