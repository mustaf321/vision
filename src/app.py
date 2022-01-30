from fastapi import FastAPI

import uvicorn
from db import db_handel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from routers import alarms, nodes,measurements
from fastapi import WebSocket, WebSocketDisconnect
from websocket.broadcaster import manager
from core.engine import monitoring ,defuse_alarm
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(alarms.router)
app.include_router(nodes.router)
app.include_router(measurements.router)
db =[]

class Measurement(BaseModel):
    nodeid: int
    temperature : float
    humidity : float
    SingleDS18B20 : float




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

