# File: backend/app/db/seed.py
from sqlalchemy.orm import Session
from app.crud.authsystem.user import crud_user
from app.schemas.authsystem.user import UserCreate
from app.core.security import get_password_hash

async def create_test_users(db: Session) -> None:
    """Create test users for development"""
    test_users = [
        {
            "email": "admin@fieldtrax.com",
            "password": "admin123",  # You should change this in production
            "username": "admin",
            "full_name": "Admin User",
            "is_admin": True,
            "is_active": True,
            "is_verified": True
        },
        {
            "email": "user@fieldtrax.com",
            "password": "user123",  # You should change this in production
            "username": "testuser",
            "full_name": "Test User",
            "is_admin": False,
            "is_active": True,
            "is_verified": True
        }
    ]

    for user_data in test_users:
        # Check if user exists
        existing_user = crud_user.get_by_email(db, email=user_data["email"])
        if not existing_user:
            user_in = UserCreate(**user_data)
            crud_user.create(db, obj_in=user_in)
            print(f"Created test user: {user_data['email']}")

