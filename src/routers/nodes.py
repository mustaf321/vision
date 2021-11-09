from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse 
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from engine.engine import remove_node,add_node,get_all_nodes,get_node
router = APIRouter(

    prefix="/nodes",
    tags=["nodes"],
    responses={404:{"description":"No node found", "detail": "No node found"}}
)

class Details(BaseModel):
    location: str
    ip: str
    name: str
    
    
@router.get("/list")
async def listnodes():
    result = get_all_nodes()
    print(result)
    result=jsonable_encoder(result)
    return JSONResponse(content=result)

@router.get("/{nodeid}")
async def getnode(nodeid: int):
    result = get_node(nodeid)

    if result is None:
        raise HTTPException(status_code = 404)
    return JSONResponse(content=jsonable_encoder(result))    

@router.post("/{nodeid}")
async def addnode(nodeid:int,details:Details):
    node_exists = add_node(nodeid,details)
    if node_exists:
        return HTTPException(status_code = 400)
    else:
        return JSONResponse(content={"status":"ok"})


@router.delete("/{nodeid}")
async def deletenode(nodeid: int):
    is_deleted = remove_node(nodeid)
    if is_deleted:
        return JSONResponse(content={"status":"ok"})
    else:
        raise HTTPException(status_code = 404)
        