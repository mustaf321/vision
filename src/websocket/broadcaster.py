from fastapi import WebSocket
from pydantic import BaseModel
import json
from typing import List


class Alarm(BaseModel):
    nodeid:int
    min : float
    max : float
    status: bool




class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print("Client connected")
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print("Client disconnected")
        self.active_connections.remove(websocket)

    async def broadcast(self, type: str, message: dict):
        for connection in self.active_connections:
            message["type"] = type
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


async def broadcast_new_alarm(alram: Alarm):
    await manager.broadcast("NEW_ALARM", { "nodeid":alram.nodeid,"max": alram.max, "min":alram.min,"status":alram.status})

async def broadcast_new_node(nodeid:int):
    await manager.broadcast("NEW_NODE", { "nodeid":nodeid})    