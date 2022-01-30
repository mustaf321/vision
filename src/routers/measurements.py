from typing import List
from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.engine import add_measurement,get_all_measurements
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


@router.get('/list')
def list_measurements():
   c =  get_all_measurements()
  # monitoring()
   return jsonable_encoder(c) 

@router.get('/api/v1/measurements/{measurment_id}')
async def get_measurement(measurment_id: int):
    print(measurment_id)
    return True


@router.put('/api/v1/temperatures/{nodeid}' )
async def update_measurement(nodeid: int, measurement : Measurement):
  await add_measurement(nodeid, measurement)


    