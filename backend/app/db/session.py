# File: backend/app/db/session.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
import os
from app.models.base import Base

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc://sa:admin@localhost:1433/FTServer?driver=ODBC+Driver+17+for+SQL+Server")
    SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./offline.db")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()

# Define offline database path
OFFLINE_DB_DIR = Path(__file__).parent.parent / 'offline_db'

# Create default engine for compatibility
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        # Initialize both engines
        self.online_engine = self._create_online_engine()
        self.offline_engine = None  # Will be created only when needed
        
        # Set MSSQL as the default engine
        self.current_engine = self.online_engine
        self.is_online = True
        self._session_factory = None
        self._initialized = True
        
        # Check connection immediately
        self.check_online_connection()

    def _create_online_engine(self):
        return create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600
        )

    def _create_offline_engine(self):
        """Create SQLite engine only when needed"""
        if not OFFLINE_DB_DIR.exists():
            OFFLINE_DB_DIR.mkdir(parents=True)
            print("Created offline database directory")
        
        sqlite_path = OFFLINE_DB_DIR / 'offline.db'
        return create_engine(
            f"sqlite:///{sqlite_path}",
            connect_args={"check_same_thread": False}
        )

    def _create_tables(self):
        """Create tables in databases"""
        try:
            print("Creating tables in online database...")
            Base.metadata.create_all(bind=self.online_engine)
            print("Online tables created.")
        except Exception as e:
            print(f"Could not create online tables: {e}")
            
            # Initialize offline engine if needed
            if self.offline_engine is None:
                self.offline_engine = self._create_offline_engine()
                
            print("Creating tables in offline database...")
            Base.metadata.create_all(bind=self.offline_engine)
            print("Offline tables created.")

    def check_online_connection(self) -> bool:
        """Try to establish online connection"""
        try:
            with self.online_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            self.current_engine = self.online_engine
            self.is_online = True
            self._update_session_factory()
            print("Successfully connected to MSSQL")
            return True
        except Exception as e:
            print(f"Failed to connect to MSSQL: {e}")
            # Initialize offline engine only when needed
            if self.offline_engine is None:
                self.offline_engine = self._create_offline_engine()
            self.current_engine = self.offline_engine
            self.is_online = False
            self._update_session_factory()
            return False

    def _update_session_factory(self):
        """Update session factory when engine changes"""
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.current_engine
        )

    def get_session_maker(self):
        """Get session maker for current engine"""
        if self._session_factory is None:
            self._update_session_factory()
        return self._session_factory

    @property
    def current_db_engine(self):
        """Get the current active engine"""
        return self.current_engine

# Create and export global instances
db_manager = DatabaseManager()
SessionLocal = db_manager.get_session_maker()

@asynccontextmanager
async def get_db() -> AsyncGenerator[Session, None]:
    """
    Provide a transactional scope around a series of operations.
    Returns a Generator that yields a Session.
    """
    db = SessionLocal()
    try:
        # Try to connect online at the start of each session
        if db_manager.check_online_connection():
            # If online connection is successful, get a new session with the online engine
            db.close()  # Close the old session
            db = db_manager.get_session_maker()()  # Get new session with current engine
        yield db
    finally:
        db.close()

# Make sure we export everything needed
__all__ = ['db_manager', 'SessionLocal', 'get_db', 'engine']