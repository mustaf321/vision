from fastapi import WebSocket
from pydantic import BaseModel
import json
from typing import List


class Alarm(BaseModel):
    nodeid:int
    min : float
    max : float
    status: bool

class Measurement(BaseModel):
    nodeid: int
    temperature : float
    humidity : float
    SingleDS18B20 : float


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
        data = {}
        data["type"] = type
        data["content"] = message
        print(data)
        for connection in self.active_connections:

            print("messege forwordet")
            print(data)
            await connection.send_text(json.dumps(data))


manager = ConnectionManager()


async def broadcast_new_alarm(alarm: Alarm):
    await manager.broadcast("NEW_ALARM", { "nodeid":alarm.nodeid,"max": alarm.max, "min":alarm.min,"status":alarm.status})

async def broadcast_new_node(nodeid:int):
    await manager.broadcast("NEW_NODE", { "nodeid":nodeid})    


async def broadcast_new_measurement(measurement: Measurement):
    await manager.broadcast("NEW_MEASUREMENT", { "nodeid":measurement.nodeid,  "TEMP": measurement.temperature,"HUIM":measurement.humidity,"SingleDS18B20":measurement.SingleDS18B20 })   