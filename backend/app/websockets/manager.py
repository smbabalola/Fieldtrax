# app/websockets/manager.py
from typing import Dict, List, Optional
from fastapi import WebSocket
from uuid import UUID
import logging
import json
from datetime import datetime

from app.schemas.events import JobEvent, EventType

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasting for real-time job updates
    """
    def __init__(self):
        # Active connections per job
        self.active_connections: Dict[UUID, List[WebSocket]] = {}
        # User connections mapping
        self.user_connections: Dict[str, List[WebSocket]] = {}
        # Connection to user mapping
        self.connection_user_map: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, job_id: UUID, user_id: str):
        """
        Connect a client to a specific job's updates
        """
        try:
            await websocket.accept()
            
            # Initialize job connections if needed
            if job_id not in self.active_connections:
                self.active_connections[job_id] = []
            self.active_connections[job_id].append(websocket)
            
            # Initialize user connections if needed
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
            
            # Map connection to user
            self.connection_user_map[websocket] = user_id
            
            # Log connection
            logger.info(f"User {user_id} connected to job {job_id}")
            
            # Notify other users about the new connection
            await self.broadcast_to_job(
                job_id,
                JobEvent(
                    type=EventType.USER_JOINED,
                    job_id=job_id,
                    user_id=user_id,
                    timestamp=datetime.utcnow(),
                    data={"message": f"User {user_id} joined"}
                )
            )
            
        except Exception as e:
            logger.error(f"Error connecting websocket: {str(e)}")
            raise

    async def disconnect(self, websocket: WebSocket):
        """
        Disconnect a client and clean up all references
        """
        try:
            # Get user ID before removing mappings
            user_id = self.connection_user_map.get(websocket)
            
            # Remove from job connections
            for job_id, connections in self.active_connections.items():
                if websocket in connections:
                    connections.remove(websocket)
                    if not connections:
                        del self.active_connections[job_id]
                    
                    # Notify others about disconnection
                    if user_id:
                        await self.broadcast_to_job(
                            job_id,
                            JobEvent(
                                type=EventType.USER_LEFT,
                                job_id=job_id,
                                user_id=user_id,
                                timestamp=datetime.utcnow(),
                                data={"message": f"User {user_id} left"}
                            )
                        )
            
            # Remove from user connections
            if user_id:
                if user_id in self.user_connections:
                    self.user_connections[user_id].remove(websocket)
                    if not self.user_connections[user_id]:
                        del self.user_connections[user_id]
            
            # Remove from connection map
            if websocket in self.connection_user_map:
                del self.connection_user_map[websocket]
                
            logger.info(f"User {user_id} disconnected")
            
        except Exception as e:
            logger.error(f"Error disconnecting websocket: {str(e)}")
            raise

    async def broadcast_to_job(self, job_id: UUID, event: JobEvent):
        """
        Broadcast event to all clients connected to a specific job
        """
        if job_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[job_id]:
                try:
                    await connection.send_json(event.dict())
                except Exception as e:
                    logger.error(f"Error broadcasting to connection: {str(e)}")
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                await self.disconnect(connection)

    async def send_personal_message(self, user_id: str, message: str):
        """
        Send a message to a specific user across all their connections
        """
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
                await self.disconnect(connection)

    async def broadcast_system_message(self, message: str):
        """
        Broadcast a system message to all connected clients
        """
        all_connections = set()
        for connections in self.active_connections.values():
            all_connections.update(connections)
        
        disconnected = []
        for connection in all_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting system message: {str(e)}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            await self.disconnect(connection)

# Create a global instance of the connection manager
job_update_manager = ConnectionManager()

# app/api/deps.py
from typing import Generator
from fastapi import Depends

from app.websockets.manager import job_update_manager

async def get_job_update_manager() -> ConnectionManager:
    """
    Dependency to get the WebSocket connection manager
    """
    return job_update_manager

# app/api/endpoints/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.api.deps import get_job_update_manager
from app.core.security import get_current_user_ws
from uuid import UUID

router = APIRouter()

@router.websocket("/ws/{job_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    job_id: UUID,
    manager: ConnectionManager = Depends(get_job_update_manager),
    current_user = Depends(get_current_user_ws)
):
    try:
        await manager.connect(websocket, job_id, current_user.id)
        try:
            while True:
                data = await websocket.receive_text()
                # Process received data
                await manager.broadcast_to_job(
                    job_id,
                    JobEvent(
                        type=EventType.JOB_UPDATED,
                        job_id=job_id,
                        user_id=current_user.id,
                        timestamp=datetime.utcnow(),
                        data={"message": data}
                    )
                )
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        try:
            await websocket.close()
        except:
            pass