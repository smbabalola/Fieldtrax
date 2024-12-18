# app/core/config.py
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FieldTrax"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React development server
        "http://localhost:5173",  # Vite development server
    ]
    
    # Database Settings
    DB_SERVER: str = Field("localhost", description="Database server host")
    DB_PORT: str = Field("1433", description="Database server port")
    DB_USER: str = Field(..., description="Database username")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_NAME: str = Field(..., description="Database name")
    DB_DRIVER: str = Field("ODBC Driver 17 for SQL Server", description="SQL Server ODBC driver")

    @property
    def DATABASE_URL(self) -> str:
        # Construct database URL with proper encoding of special characters
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"
            f"?driver={self.DB_DRIVER.replace(' ', '+')}"
        )
    
    # JWT Settings
    SECRET_KEY: str = Field(..., description="Secret key for JWT encoding")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, description="Access token expiry in minutes")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, description="Refresh token expiry in days")
    RESET_TOKEN_EXPIRE_HOURS: int = Field(24, description="Password reset token expiry in hours")
    
    
    # Email Settings
    MAIL_USERNAME: str = Field("", description="SMTP username")
    MAIL_PASSWORD: str = Field("", description="SMTP password")
    MAIL_FROM: str = Field("noreply@fieldtrax.com", description="Default from email")
    MAIL_PORT: int = Field(587, description="SMTP port")
    MAIL_SERVER: str = Field("smtp.gmail.com", description="SMTP server")
    MAIL_STARTTLS: bool = Field(True, description="Use STARTTLS")
    MAIL_SSL_TLS: bool = Field(False, description="Use SSL/TLS")
    MAIL_USE_CREDENTIALS: bool = Field(True, description="Use SMTP authentication")
    MAIL_VALIDATE_CERTS: bool = Field(True, description="Validate SSL certificates")
    
    # Frontend URL
    FRONTEND_URL: str = Field("http://localhost:3000", description="Frontend application URL")

    # Add SQLite settings
    SQLITE_DB_PATH: str = Field("app/offline_db/offline.db", description="SQLite database path")
    
    @property
    def SQLITE_DATABASE_URL(self) -> str:
        return f"sqlite:///{self.SQLITE_DB_PATH}"
    
    # Additional Settings
    DEBUG: bool = Field(False, description="Debug mode")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()