# # app/__init__.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# # from app.api.v1.api import api_router
# from app.db.init_db import init_db
# # app/db/init_db.py
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     description="FieldTrax API",
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc",
#     openapi_url="/openapi.json"
# )

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include API router with prefix
# app.include_router(api_router, prefix=settings.API_V1_STR)

# Add a redirect from root to docs
# from fastapi.responses import RedirectResponse

# @app.get("/", include_in_schema=False)
# async def root():
#     return RedirectResponse(url="/docs")

# @app.on_event("startup")
# async def startup_event():
#     logger.info("Initializing database...")
#     init_db()
#     logger.info("Database initialized successfully")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)