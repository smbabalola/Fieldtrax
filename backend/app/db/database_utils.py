# File: backend/app/db/database_utils.py
from pathlib import Path

# Create offline database directory
OFFLINE_DB_DIR = Path(__file__).parent.parent / 'offline_db'
OFFLINE_DB_DIR.mkdir(exist_ok=True)