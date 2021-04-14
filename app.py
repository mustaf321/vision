from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
app = FastAPI()
db =[]

class Measurement(BaseModel):
    senorID: str
    temperature : str
    humidity : str

@app.get('/api/v1/measurements/measurment')
async def measurements():
    return db

@app.get('/api/v1/measurements/{measurment_id}')
async def get_measurement(measurment_id: int):
    print(measurment_id)
    return db[measurment_id] 

@app.put('/api/v1/temperatures' )
def add_tempetratur( measurement : Measurement):
 db.append(measurement.dict())
 return db[-1]

@app.delete('/api/v1/measurements/{measurment_id}')
async def delet_measurement(measurment_id: int):
    print(measurment_id)
    db.pop(measurment_id -1)
    return {'measurement deleted'}


if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port="8080")    
    