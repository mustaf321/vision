from fastapi import FastAPI
import uvicorn
import json

#Init
app = FastAPI(debug=True)

with open("teperatur.json") as f:
    teperatur = json.load(f)


@app.get('/api/v1/temperatur')
async def get_temperatur():
    return{"temperaur":teperatur}    

if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port="8080")    