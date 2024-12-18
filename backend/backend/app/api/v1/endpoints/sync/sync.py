# File: backend/app/api/v1/endpoints/sync/sync.py
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.sync_manager import sync_manager

router = APIRouter()

@router.post("/sync")
async def sync_data(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Synchronize offline data with online database"""
    background_tasks.add_task(sync_manager.sync_to_online, db)
    return {"message": "Synchronization started"}

@router.get("/sync/status")
async def get_sync_status():
    """Get current synchronization status"""
    pending = len([c for c in sync_manager.pending_changes if not c['synced']])
    return {
        "pending_changes": pending,
        "is_online": sync_manager.db_manager.is_online
    }
