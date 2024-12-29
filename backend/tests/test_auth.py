import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.core.security import create_access_token, get_password_hash
from app.models.auth import User
from app.models.role import Role, RoleType
from app.core.config import settings

def test_create_user(test_client, test_db):
    # Create a test role first
    role = Role(
        name=RoleType.FIELD_ENGINEER,
        description="Field Engineer Role"
    )
    test_db.add(role)
    test_db.commit()

    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "TestPass123!",
            "username": "testuser",
            "full_name": "Test User",
            "role": RoleType.FIELD_ENGINEER
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "password" not in data

def test_login_success(test_client, test_db):
    # Create test user with role
    hashed_password = get_password_hash("TestPass123!")
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=hashed_password,
        role_id=role.id
    )
    test_db.add(user)
    test_db.commit()

    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "TestPass123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(test_client):
    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()

def test_get_current_user(test_client, test_db):
    # Create test user with role
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.commit()

    # Create access token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=15)
    )

    response = test_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "role" in data

def test_session_management(test_client, test_db):
    # Create test user with role
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.commit()

    # Login to create first session
    response1 = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "TestPass123!"
        }
    )
    assert response1.status_code == 200
    token1 = response1.json()["access_token"]

    # Try to login again (should invalidate first session)
    response2 = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "TestPass123!"
        }
    )
    assert response2.status_code == 200
    token2 = response2.json()["access_token"]

    # First token should no longer work
    response3 = test_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response3.status_code == 401

    # New token should work
    response4 = test_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response4.status_code == 200

def test_role_based_access(test_client, test_db):
    # Create admin role and user
    admin_role = Role(name=RoleType.ADMIN)
    test_db.add(admin_role)
    test_db.flush()
    
    admin_user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("AdminPass123!"),
        role_id=admin_role.id
    )
    test_db.add(admin_user)
    
    # Create engineer role and user
    engineer_role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(engineer_role)
    test_db.flush()
    
    engineer_user = User(
        email="engineer@example.com",
        username="engineer",
        hashed_password=get_password_hash("EngineerPass123!"),
        role_id=engineer_role.id
    )
    test_db.add(engineer_user)
    test_db.commit()

    # Login as admin
    admin_response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "AdminPass123!"
        }
    )
    admin_token = admin_response.json()["access_token"]

    # Login as engineer
    engineer_response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "engineer",
            "password": "EngineerPass123!"
        }
    )
    engineer_token = engineer_response.json()["access_token"]

    # Test admin-only endpoint
    admin_only_response = test_client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_only_response.status_code == 200

    # Test same endpoint with engineer token
    engineer_forbidden_response = test_client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {engineer_token}"}
    )
    assert engineer_forbidden_response.status_code == 403