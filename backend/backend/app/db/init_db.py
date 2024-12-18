# File: backend/app/db/init_db.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import insert, create_engine
from app.core.config import Settings
from app.core.security import get_password_hash
from app.crud.authsystem.user import crud_user
from app.models.authsystem.user import User
from app.models.authsystem.role import Role
from app.models.authsystem.associations import user_roles_table
from app.schemas.authsystem.user import UserCreate
from app.database import Base, engine

def create_tables() -> None:
    """Create all tables in the database"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

def init_db(db: Session) -> None:
    """Initialize the database with initial data"""
    try:
        # First ensure tables exist
        create_tables()

        print("Checking if admin user: admin@fieldtrax.com exists.")
        admin_user = db.query(User).filter(User.email == "admin@fieldtrax.com").first()
        
        if not admin_user:
            print("Creating admin user: admin@fieldtrax.com")
            admin_user = User(
                email="admin@fieldtrax.com",
                username="admin",
                password=get_password_hash("admin123"),
                full_name="Admin User",
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            # Create admin role if it doesn't exist
            admin_role = db.query(Role).filter(Role.name == "admin").first()
            if not admin_role:
                admin_role = Role(
                    name="admin",
                    description="Administrator role with full access"
                )
                db.add(admin_role)
                db.commit()
                db.refresh(admin_role)

            # Associate admin user with admin role
            stmt = insert(user_roles_table).values(
                user_id=admin_user.id,
                role_id=admin_role.id
            )
            db.execute(stmt)
            db.commit()

            print("Admin user and role created and associated successfully.")
        else:
            print("Admin user already exists.")

        print("Admin user initialization complete.")
    except Exception as e:
        print(f"Error in init_db: {e}")
        db.rollback()
        raise