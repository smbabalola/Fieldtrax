# File: backend/app/core/management/commands/check_db.py
import click
from app.db.session import db_manager, get_db

@click.command()
def check_db():
    """Check database connection status"""
    print("Checking database connection...")
    with get_db() as db:
        is_online = db_manager.check_online_connection()
        print(f"Using {'MSSQL' if is_online else 'SQLite'} database")
        
        if is_online:
            print("Successfully connected to MSSQL Server")
        else:
            print("Using offline SQLite database")
            print("MSSQL Server connection not available")

# Usage: python -m app.core.management.commands.check_db