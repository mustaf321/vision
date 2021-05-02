from fastapi import FastAPI
import uvicorn
import db_handel
from pydantic import BaseModel
app = FastAPI()
db =[]

class Measurement(BaseModel):
    sensorID: int
    temperature : float
    humidity : float
    SingleDS18B20 : float

@app.get('/api/v1/measurements/measurment')
async def measurements():
    return db

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
  k = db_handel.add_tempetratur("mesungen",measurement.sensorID,measurement.temperature,measurement.humidity,measurement.SingleDS18B20)
  print(k)
  db[sensorID] = measurement.dict() 
  print(db[sensorID])
  return db[sensorID]

@app.delete('/api/v1/measurements/{measurment_id}')
async def delet_measurement(measurment_id: int):
    print(measurment_id)
    db.pop(measurment_id -1)
    return {'measurement deleted'}
   
    