# /backend/tests/test_password_reset.py
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.models.auth import User, PasswordReset
from app.models.role import Role, RoleType
from app.core.security import get_password_hash

def test_request_password_reset(test_client, test_db):
    # Create test user
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("OldPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.commit()

    response = test_client.post(
        "/api/v1/auth/request-reset",
        json={"email": "testuser@example.com"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "If your email is registered, you will receive a password reset link"
    
    # Verify reset token was created
    reset_token = test_db.query(PasswordReset).filter_by(user_id=user.id).first()
    assert reset_token is not None
    assert not reset_token.is_used

def test_verify_reset_token(test_client, test_db):
    # Create test user and reset token
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("OldPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.flush()

    reset_token = PasswordReset(
        user_id=user.id,
        token="valid_token",
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    test_db.add(reset_token)
    test_db.commit()

    # Test valid token
    response = test_client.get("/api/v1/auth/verify-token/valid_token")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Test invalid token
    response = test_client.get("/api/v1/auth/verify-token/invalid_token")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired reset token"

def test_reset_password(test_client, test_db):
    # Create test user and reset token
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("OldPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.flush()

    reset_token = PasswordReset(
        user_id=user.id,
        token="valid_token",
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    test_db.add(reset_token)
    test_db.commit()

    # Test password reset
    response = test_client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "valid_token",
            "new_password": "NewPass123!"
        }
    )
    
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify new password works
    login_response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "NewPass123!"
        }
    )
    assert login_response.status_code == 200

def test_expired_token(test_client, test_db):
    # Create test user and expired reset token
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("OldPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.flush()

    expired_token = PasswordReset(
        user_id=user.id,
        token="expired_token",
        expires_at=datetime.utcnow() - timedelta(hours=1)
    )
    test_db.add(expired_token)
    test_db.commit()

    response = test_client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "expired_token",
            "new_password": "NewPass123!"
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired reset token"

def test_used_token(test_client, test_db):
    # Create test user and used reset token
    role = Role(name=RoleType.FIELD_ENGINEER)
    test_db.add(role)
    test_db.flush()
    
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=get_password_hash("OldPass123!"),
        role_id=role.id
    )
    test_db.add(user)
    test_db.flush()

    used_token = PasswordReset(
        user_id=user.id,
        token="used_token",
        expires_at=datetime.utcnow() + timedelta(hours=1),
        is_used=True
    )
    test_db.add(used_token)
    test_db.commit()

    response = test_client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "used_token",
            "new_password": "NewPass123!"
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired reset token"