# File: backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Import database modules
from app.db.session import db_manager, get_db, SessionLocal
from app.db.base import Base

# Import configurations and core modules
from app.core.config import settings
from app.core.cache import init_cache
from app.db.init_db import init_db
from fastapi.openapi.utils import get_openapi

# Import API router
from app.api.v1.api import api_router

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="FieldTrax API",
        version="1.0.0",
        description="Backend API for FieldTrax application",
        routes=app.routes,
    )
    
    # Add security scheme to OpenAPI schema
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "api/v1/token",
                    "scopes": {}
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Print the database URL to verify the path
print(f"Using database URL: {settings.DATABASE_URL}")

# Create database tables
db_manager._create_tables()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Testing database connection...")
    db = SessionLocal()
    try:
        is_online = db_manager.check_online_connection()
        print(f"Using {'MSSQL' if is_online else 'SQLite'} database")
        
        # Initialize cache
        await init_cache()
        
        # Initialize database with test data if in development
        if settings.ENVIRONMENT == "development":
            try:
                init_db(db)
                print("Development database initialized with test data")
            except Exception as e:
                print(f"Error initializing development database: {str(e)}")
    finally:
        db.close()

    yield

# Initialize FastAPI app
app = FastAPI(
    title="FieldTrax API",
    description="Backend API for FieldTrax application",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://www.localhost:3000"],  # Add both domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Include API router with version prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    is_online = db_manager.check_online_connection()
    return {
        "status": "healthy",
        "database": {
            "type": "MSSQL" if is_online else "SQLite",
            "is_online": is_online,
            "connection_status": "connected"
        }
    }

@app.get("/debug/routes")
async def debug_routes():
    """Endpoint to help debug available routes"""
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": route.methods
        })
    return {"routes": routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)