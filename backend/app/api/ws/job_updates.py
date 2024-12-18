# app/api/ws/job_updates.py
from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List, Any
import json
import logging
from uuid import UUID

from app.core.security import get_current_user_ws
from app.schemas.events import JobEvent, EventType
from app.core.config import settings

logger = logging.getLogger(__name__)

class JobUpdateManager:
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}
        self.user_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, job_id: UUID, user_id: str):
        await websocket.accept()
        if job_id not in self.active_connections:
            self.active_connections[job_id] = []
        self.active_connections[job_id].append(websocket)
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, job_id: UUID, user_id: str):
        if job_id in self.active_connections:
            self.active_connections[job_id].remove(websocket)
            if not self.active_connections[job_id]:
                del self.active_connections[job_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def broadcast_to_job(self, job_id: UUID, event: JobEvent):
        if job_id in self.active_connections:
            for connection in self.active_connections[job_id]:
                try:
                    await connection.send_json(event.dict())
                except Exception as e:
                    logger.error(f"Error broadcasting to connection: {str(e)}")

    async def send_personal_message(self, user_id: str, message: str):
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending personal message: {str(e)}")

job_update_manager = JobUpdateManager()

# WebSocket route handler
async def job_websocket_endpoint(
    websocket: WebSocket,
    job_id: UUID,
    current_user = Depends(get_current_user_ws)
):
    try:
        await job_update_manager.connect(websocket, job_id, current_user.id)
        # Notify other users that someone joined
        join_event = JobEvent(
            type=EventType.USER_JOINED,
            job_id=job_id,
            user_id=current_user.id,
            data={"username": current_user.username}
        )
        await job_update_manager.broadcast_to_job(job_id, join_event)
        
        try:
            while True:
                data = await websocket.receive_text()
                event_data = json.loads(data)
                event = JobEvent(**event_data)
                await job_update_manager.broadcast_to_job(job_id, event)
                
        except WebSocketDisconnect:
            await job_update_manager.disconnect(websocket, job_id, current_user.id)
            leave_event = JobEvent(
                type=EventType.USER_LEFT,
                job_id=job_id,
                user_id=current_user.id,
                data={"username": current_user.username}
            )
            await job_update_manager.broadcast_to_job(job_id, leave_event)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1001)

