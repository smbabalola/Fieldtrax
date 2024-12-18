# # app/__init__.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# # from app.api.v1.api import api_router
# from app.db.init_db import init_db
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     description="FieldTrax API",
#     version="1.0.0",
#     docs_url="/api/docs",
#     redoc_url="/api/redoc",
#     openapi_url="/api/openapi.json"
# )

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API router
# # app.include_router(api_router, prefix=settings.API_V1_STR)

# # Initialize database on startup
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Initializing database...")
#     init_db()
#     logger.info("Database initialized successfully")