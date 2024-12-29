import sys
import os

# Adjust the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.auth import User
from app.core.auth import get_password_hash

# Ensure that you have imported your models correctly
Base.metadata.create_all(bind=engine)

def create_first_user():
    with SessionLocal() as session:
        # Check if user already exists
        existing_user = session.query(User).filter(User.username == "testuser").first()
        if existing_user:
            print("User already exists.")
            return

        # Create new user with hashed password
        hashed_password = get_password_hash("Password123!")
        new_user = User(
            username="testuser",
            hashed_password=hashed_password,
            email="testuser@example.com",
            is_active=True
        )
        session.add(new_user)
        session.commit()
        print("First user created successfully.")

if __name__ == "__main__":
    create_first_user()

