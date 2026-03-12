from typing import Set
from fastapi import WebSocket
import json
import asyncio

class WebSocketManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_location_update(self, location_data: dict):
        message = {
            "type": "location_update",
            "data": location_data
        }
        await self.broadcast(message)

manager = WebSocketManager()
