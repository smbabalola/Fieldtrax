# app/api/v1/endpoints/ws.py
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, logger
from typing import Optional
from uuid import UUID

from app.core.security import get_current_user_ws
from app.api.deps import get_job_update_manager
from app.models.events import JobEvent, EventType

router = APIRouter()

@router.websocket("/jobs/{job_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    job_id: UUID,
    manager = Depends(get_job_update_manager),
    current_user = Depends(get_current_user_ws)
):
    """WebSocket endpoint for real-time job updates"""
    try:
        await manager.connect(websocket, job_id, current_user.id)
        
        while True:
            try:
                data = await websocket.receive_json()
                event = JobEvent(**data)
                await manager.broadcast_to_job(job_id, event)
                
            except WebSocketDisconnect:
                await manager.disconnect(websocket, job_id, current_user.id)
                break
                
            except Exception as e:
                await manager.broadcast_to_job(
                    job_id,
                    JobEvent(
                        type=EventType.ERROR,
                        job_id=job_id,
                        user_id=current_user.id,
                        timestamp=datetime.now(),
                        data={"error": str(e)}
                    )
                )
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1001)