from fastapi import FastAPI

import uvicorn
from db import db_handel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from routers import alarms, nodes
from fastapi import WebSocket, WebSocketDisconnect
from websocket.broadcaster import manager
from engine.engine import monitoring ,defuse_alarm
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(alarms.router)
app.include_router(nodes.router)
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


@app.get('/measurements/list')
def measurements():
   c =   db_handel.get_mesuremnt()
   
   monitoring()
   return jsonable_encoder(c)

@app.get('/api/v1/measurements/{measurment_id}')
async def get_measurement(measurment_id: int):
    print(measurment_id)
    return db[measurment_id] 

@app.post('/api/v1/temperatures' )
def add_tempetratur( measurement : Measurement):
 db.append(measurement.dict())
 return db[-1]

@app.put('/api/v1/temperatures/{nodeid}' )
def update_measurement(nodeid: int, measurement : Measurement):
  k = db_handel.add_tempetratur("mesungen",nodeid,measurement.temperature,measurement.humidity,measurement.SingleDS18B20)
  print(k)


@app.delete('/api/v1/measurements/{measurment_id}')
async def delet_measurement(measurment_id: int):
    print(measurment_id)
    db.pop(measurment_id -1)
    return {'measurement deleted'}
   
    