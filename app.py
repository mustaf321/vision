from fastapi import FastAPI
import uvicorn
import db_handel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
app = FastAPI()
origins = [
    
    "http://localhost:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db =[]

class Measurement(BaseModel):
    sensorid: int
    temperature : float
    humidity : float
    SingleDS18B20 : float

@app.get('/api/v1/measurements/measurment')
def measurements():
   c =   db_handel.get_mesuremnt()
   print(c)
   return jsonable_encoder(c)

@app.get('/api/v1/measurements/{measurment_id}')
async def get_measurement(measurment_id: int):
    print(measurment_id)
    return db[measurment_id] 

@app.post('/api/v1/temperatures' )
def add_tempetratur( measurement : Measurement):
 db.append(measurement.dict())
 return db[-1]

@app.put('/api/v1/temperatures/{sensorID}' )
def update_measurement(sensorID: int, measurement : Measurement):
  k = db_handel.add_tempetratur("mesungen",measurement.sensorid,measurement.temperature,measurement.humidity,measurement.SingleDS18B20)
  print(k)
  db[sensorid] = measurement.dict() 
  print(db[sensorid])
  return db[sensorid]

@app.delete('/api/v1/measurements/{measurment_id}')
async def delet_measurement(measurment_id: int):
    print(measurment_id)
    db.pop(measurment_id -1)
    return {'measurement deleted'}
   
    