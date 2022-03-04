from typing import List
from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.engine import defuse_alarm, get_all_alarms, received_new_alarm, get_alarm, remove_alarm
from fastapi.encoders import jsonable_encoder
router = APIRouter(

    prefix="/alarms",
    tags=["alarms"],
    responses={404: {"description": "No alarm found", "detail": "No alarm found"}}
)


class Alarm(BaseModel):
    nodeid: int
    min:  float
    max: float
    min_hium:  float
    max_hium: float
    status: bool


@router.get("/list", response_model=List[str])
async def listalarms():
    result = get_all_alarms()
    result = jsonable_encoder(result)
    return JSONResponse(content=result)


@router.get("/{nodeid}")
async def getalarm(nodeid: int):
    result = get_alarm(nodeid)
    if result is None:
        raise HTTPException(status_code=404)
    return JSONResponse(content=jsonable_encoder(result))


@router.post("")
async def setalarm(alarm: Alarm):
    node_exists = await received_new_alarm(alarm)
    if node_exists:
        return JSONResponse(content={"status": "ok"})
    else:
        raise HTTPException(status_code=404)


@router.post("/defuse/{nodeid}")
async def setalarm(nodeid: int):
    node_exists = await defuse_alarm(nodeid)

    if node_exists:

        return JSONResponse(content={"status": "defused alam"})
    else:
        raise HTTPException(status_code=404)


@router.delete("/{nodeid}")
async def deletealarm(nodeid: int):
    is_deleted = await remove_alarm(nodeid)
    if is_deleted:
        return JSONResponse(content={"status": "ok"})
    else:
        raise HTTPException(status_code=404)
