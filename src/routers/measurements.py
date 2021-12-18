from typing import List
from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from engine.engine import monitoring ,defuse_alarm, get_all_alarms, received_new_alarm, get_alarm, remove_alarm
from fastapi.encoders import jsonable_encoder
router = APIRouter(

    prefix="/measurements",
    tags=["measurements"],
    responses={404: {"description": "No node found", "detail": "No node found"}}
)
class Measurement(BaseModel):
    nodeid: int
    temperature : float
    humidity : float
    SingleDS18B20 : float


@router.get('/measurements/list')
def measurements():
   c =   db_handel.get_mesuremnt()
   
   monitoring()
   return jsonable_encoder(c) 

@router.get('/api/v1/measurements/{measurment_id}')
async def get_measurement(measurment_id: int):
    print(measurment_id)
    return db[measurment_id] 

@router.post('/api/v1/temperatures' )
def add_tempetratur( measurement : Measurement):
 db.routerend(measurement.dict())
 return db[-1]

@router.put('/api/v1/temperatures/{nodeid}' )
def update_measurement(nodeid: int, measurement : Measurement):
  k = db_handel.add_tempetratur("mesungen",nodeid,measurement.temperature,measurement.humidity,measurement.SingleDS18B20)
  print(k)


@router.delete('/api/v1/measurements/{measurment_id}')
async def delet_measurement(measurment_id: int):
    print(measurment_id)
    db.pop(measurment_id -1)
    return {'measurement deleted'}
   
    