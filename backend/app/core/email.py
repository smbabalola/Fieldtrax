# File: backend/app/core/email.pyfrom fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr
from typing import List, Optional, Dict
from jinja2 import Environment, select_autoescape, PackageLoader
from app.core.config import settings
import os
from pathlib import Path
from datetime import datetime

# Get the absolute path to the templates directory
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_FOLDER = BASE_DIR / "templates"

# Ensure template directories exist
if not TEMPLATE_FOLDER.exists():
    TEMPLATE_FOLDER.mkdir(parents=True)
if not (TEMPLATE_FOLDER / "email").exists():
    (TEMPLATE_FOLDER / "email").mkdir()

email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=str(TEMPLATE_FOLDER)
)

class EmailService:
    def __init__(self):
        self.fastmail = FastMail(email_conf)
        self.env = Environment(
            loader=PackageLoader('app', 'templates/email'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    async def send_email(
        self,
        template_name: str,
        email: EmailStr,
        subject: str,
        template_data: Dict
    ) -> bool:
        """Generic method to send templated emails"""
        try:
            template = self.env.get_template(template_name)
            html = template.render(**template_data)

            message = MessageSchema(
                subject=subject,
                recipients=[email],
                body=html,
                subtype="html"
            )

            await self.fastmail.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending email ({template_name}): {str(e)}")
            return False

    async def send_password_reset_email(
        self, 
        email: EmailStr, 
        reset_token: str, 
        reset_link: Optional[str] = None
    ) -> bool:
        """Send password reset email with either token or direct link"""
        if not reset_link:
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        return await self.send_email(
            template_name='password_reset.html',
            email=email,
            subject="Reset Your FieldTrax Password",
            template_data={
                'reset_link': reset_link,
                'reset_token': reset_token,  # Include both for template flexibility
                'valid_hours': settings.RESET_TOKEN_EXPIRE_HOURS,
                'timestamp': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
        )

    async def send_reset_email(self, email: EmailStr, reset_link: str) -> bool:
        """Legacy method for backward compatibility"""
        return await self.send_password_reset_email(email, "", reset_link=reset_link)

    async def send_verification_email(self, email: EmailStr, verification_token: str) -> bool:
        """Send email verification link"""
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        return await self.send_email(
            template_name='email_verification.html',
            email=email,
            subject="Verify Your FieldTrax Email",
            template_data={
                'verification_link': verification_link,
                'verification_token': verification_token,
                'timestamp': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
        )

    async def send_notification(
        self,
        recipients: List[EmailStr],
        subject: str,
        body: str,
        template_data: Optional[Dict] = None
    ) -> bool:
        """Send notification email to multiple recipients"""
        try:
            if template_data:
                template = self.env.get_template('notification.html')
                html = template.render(**template_data)
            else:
                html = body

            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                body=html,
                subtype="html"
            )

            await self.fastmail.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False

# Create a global instance
email_service = EmailService()

# Export commonly used functions
send_password_reset_email = email_service.send_password_reset_email
send_reset_email = email_service.send_reset_email
send_verification_email = email_service.send_verification_email
send_notification = email_service.send_notification