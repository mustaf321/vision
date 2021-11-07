from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse 
from pydantic import BaseModel
from engine.engine import get_all_alarms, received_new_alarm
from fastapi.encoders import jsonable_encoder
router = APIRouter(

    prefix="/alarms",
    tags=["alarms"],
    responses={404:{"description":"No alarm found", "detail": "No alarm found"}}
)

class Range(BaseModel):
    min : float
    max : float

    
@router.get("/list")
async def listalarms():
    result =get_all_alarms()
    result=jsonable_encoder(result)
    return JSONResponse(content=result)

@router.get("/{sensorid}")
async def getalarm(sensorid: int):
    result =get_alarm(sensorid)

    if result is None:
        raise HTTPException(status_code = 404)
    return JSONResponse(content=jsonable_encoder(result))    

@router.post("/{sensorid}")
async def setalarm(sensorid:int,range:Range):
    node_exists = await received_new_alarm(sensorid,range)
    print(node_exists)
    
    if node_exists:
        return JSONResponse(content={"status":"ok"})
    else:
        raise HTTPException(status_code = 404)


@router.delete("/{sensorid}")
async def deletealarm(sensorid: int):
    is_deleted = delete_alarm(sensorid)
    if is_deleted:
        return JSONResponse(content={"status":"ok"})
    else:
        raise HTTPException(status_code = 404)
        