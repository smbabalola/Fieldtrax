# app/core/ws/manager.py
from fastapi import WebSocket
from typing import Dict, List, Optional
import logging
from uuid import UUID
import json
from datetime import datetime

from app.models.events import JobEvent, EventType

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time job updates"""
    
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}
        self.user_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, job_id: UUID, user_id: str):
        """Connect a client to a specific job's updates"""
        try:
            await websocket.accept()
            
            # Initialize job connections if not exists
            if job_id not in self.active_connections:
                self.active_connections[job_id] = []
            self.active_connections[job_id].append(websocket)
            
            # Track user connections
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
            
            # Notify other users about the new connection
            await self.broadcast_to_job(
                job_id,
                JobEvent(
                    type=EventType.USER_JOINED,
                    job_id=job_id,
                    user_id=user_id,
                    timestamp=datetime.utcnow(),
                    data={"message": f"User {user_id} joined the job"}
                )
            )
            
            logger.info(f"Client connected - Job: {job_id}, User: {user_id}")
            
        except Exception as e:
            logger.error(f"Error connecting client: {str(e)}")
            raise

    async def disconnect(self, websocket: WebSocket, job_id: UUID, user_id: str):
        """Disconnect a client"""
        try:
            if job_id in self.active_connections:
                self.active_connections[job_id].remove(websocket)
                if not self.active_connections[job_id]:
                    del self.active_connections[job_id]
            
            if user_id in self.user_connections:
                self.user_connections[user_id].remove(websocket)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
            
            await self.broadcast_to_job(
                job_id,
                JobEvent(
                    type=EventType.USER_LEFT,
                    job_id=job_id,
                    user_id=user_id,
                    timestamp=datetime.utcnow(),
                    data={"message": f"User {user_id} left the job"}
                )
            )
            
            logger.info(f"Client disconnected - Job: {job_id}, User: {user_id}")
            
        except Exception as e:
            logger.error(f"Error disconnecting client: {str(e)}")

    async def broadcast_to_job(self, job_id: UUID, event: JobEvent):
        """Broadcast an event to all clients connected to a specific job"""
        if job_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[job_id]:
                try:
                    await connection.send_json(event.dict())
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {str(e)}")
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                try:
                    await connection.close()
                    self.active_connections[job_id].remove(connection)
                except:
                    pass

    async def send_personal_message(self, user_id: str, message: str):
        """Send a message to a specific user"""
        if user_id in self.user_connections:
            disconnected = []
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending personal message: {str(e)}")
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                try:
                    await connection.close()
                    self.user_connections[user_id].remove(connection)
                except:
                    pass

# Create global instance
job_update_manager = ConnectionManager()

