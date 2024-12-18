# app/database.py 
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import pyodbc
import requests
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

def get_connection_string() -> str:
    """Get the database connection string with proper error handling"""
    try:
        return settings.DATABASE_URL
    except Exception as e:
        logger.error(f"Error constructing database URL: {str(e)}")
        raise

def verify_odbc_driver():
    """Verify that the specified ODBC driver is installed"""
    drivers = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    if not drivers:
        raise RuntimeError(
            "No SQL Server ODBC drivers found. Please install the Microsoft ODBC Driver for SQL Server."
        )
    if settings.DB_DRIVER not in drivers:
        logger.warning(
            f"Specified driver '{settings.DB_DRIVER}' not found. "
            f"Available drivers: {', '.join(drivers)}"
        )
        raise RuntimeError(f"Specified ODBC driver '{settings.DB_DRIVER}' not found")

def check_internet_connectivity():
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def create_db_engine():
    """Create database engine with proper error handling"""
    try:
        # Verify ODBC driver first if online
        if check_internet_connectivity():
            verify_odbc_driver()
            connection_string = f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?driver={os.getenv('DB_DRIVER')}"
        else:
            connection_string = os.getenv("OFFLINE_DATABASE_URL")
            logger.info(f"Using offline database: {connection_string}")

        # Create engine
        engine = create_engine(
            connection_string,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            pool_recycle=300
        )

        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")

        return engine
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

# Create engine
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()