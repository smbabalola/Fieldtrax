# File: backend/tests/test_db_connection.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import db_manager, get_db

def test_database_connection():
    print("Testing database connection...")
    with get_db() as db:
        is_online = db_manager.check_online_connection()
        connection_type = 'MSSQL' if is_online else 'SQLite'
        print(f"Using {connection_type} database")
        
        # Test basic query
        try:
            result = db.execute("SELECT 1").scalar()
            print(f"Test query successful: {result}")
        except Exception as e:
            print(f"Test query failed: {e}")

if __name__ == "__main__":
    test_database_connection()