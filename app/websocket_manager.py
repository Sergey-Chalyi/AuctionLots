from fastapi import WebSocket
from typing import Dict, List
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lot_id: int):
        """Accept a WebSocket connection and add it to the lot's connections."""
        await websocket.accept()
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = []
        self.active_connections[lot_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lot_id: int):
        """Remove a WebSocket connection from the lot's connections."""
        if lot_id in self.active_connections:
            self.active_connections[lot_id].remove(websocket)
            if not self.active_connections[lot_id]:
                del self.active_connections[lot_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        await websocket.send_text(message)

    async def broadcast_to_lot(self, message: str, lot_id: int):
        """Broadcast a message to all connections for a specific lot."""
        if lot_id in self.active_connections:
            disconnected_connections = []
            for connection in self.active_connections[lot_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Mark for removal if connection is broken
                    disconnected_connections.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected_connections:
                self.active_connections[lot_id].remove(connection)
            
            # Clean up empty lot connections
            if not self.active_connections[lot_id]:
                del self.active_connections[lot_id]

    async def broadcast_to_all(self, message: str):
        """Broadcast a message to all active connections."""
        for lot_id in list(self.active_connections.keys()):
            await self.broadcast_to_lot(message, lot_id)


manager = ConnectionManager()
