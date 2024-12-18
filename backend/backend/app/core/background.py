# app/core/background.py
from uuid import UUID
from fastapi import BackgroundTasks
from typing import List
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
from app.models.session import UserSession
from datetime import datetime, timezone
from sqlalchemy.orm import Session


async def notify_job_creation(job_id: UUID):
    """Send notifications when a new job is created"""
    # Email notification
    message = MIMEText(f"New job created with ID: {job_id}")
    message["Subject"] = "New Job Created"
    message["From"] = settings.MAIL_FROM
    message["To"] = settings.NOTIFICATION_EMAIL

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(message)
        
# async def cleanup_expired_sessions(db: Session):
#     """Cleanup expired and inactive sessions"""
#     now = datetime.now(timezone.utc)
#     db.query(UserSession).filter(
#         (UserSession.expires_at < now) |
#         (UserSession.last_activity < now - timedelta(minutes=30))
#     ).update({"is_active": False