# tests/api/test_jobs.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from uuid import uuid4

from .app.main import app
from app.core.security import create_access_token
from app.models.job.models import Job, JobCreate, DailyReport
from app.core.units.quantity import Depth

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {
        "id": str(uuid4()),
        "username": "testuser",
        "role": "supervisor"
    }

@pytest.fixture
def test_job():
    return {
        "id": str(uuid4()),
        "jobid": "TEST-001",
        "well_name": "TEST-WELL-01",
        "country": "US",
        "field": "TEST FIELD",
        "spuddate": datetime.utcnow().isoformat(),
        "status": "active"
    }

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(test_user)
    return {"Authorization": f"Bearer {token}"}

class TestJobEndpoints:
    def test_create_job(self, client, auth_headers, test_job):
        response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["well_name"] == test_job["well_name"]
        assert data["status"] == "active"

    def test_get_job(self, client, auth_headers, test_job):
        # First create a job
        create_response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(
            f"/api/v1/jobs/{job_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id

    def test_update_job(self, client, auth_headers, test_job):
        # Create job
        create_response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]
        
        # Update job
        update_data = {"well_name": "UPDATED-WELL"}
        response = client.put(
            f"/api/v1/jobs/{job_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["well_name"] == "UPDATED-WELL"

    def test_create_daily_report(self, client, auth_headers, test_job):
        # Create job
        create_response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]
        
        # Create daily report
        report_data = {
            "report_date": datetime.utcnow().isoformat(),
            "operations": ["Test operation"],
            "summary": "Test summary"
        }
        response = client.post(
            f"/api/v1/jobs/{job_id}/daily-reports",
            json=report_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Test summary"

class TestJobValidation:
    def test_invalid_water_depth(self, client, auth_headers, test_job):
        test_job["waterdepth"] = {"value": -100, "unit": "ft"}
        response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Water depth cannot be negative" in response.json()["detail"]

    def test_future_spud_date(self, client, auth_headers, test_job):
        test_job["spuddate"] = (datetime.utcnow() + timedelta(days=1)).isoformat()
        response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Spud date cannot be in the future" in response.json()["detail"]

class TestWebSocket:
    async def test_websocket_connection(self, client, auth_headers, test_job):
        # Create job
        create_response = client.post(
            "/api/v1/jobs/",
            json=test_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]
        
        # Connect to WebSocket
        with client.websocket_connect(
            f"/api/v1/jobs/{job