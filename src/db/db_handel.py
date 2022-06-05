from calendar import c
from datetime import datetime
import json
import os
from click import prompt
from fastapi.params import Query
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

env=1



if env == 2:
    token = "2v_GxZ7Z440aDDM4_b93Zqj4AFatIiA0bQ2SzrZQ3Zgk66uajtunvwSc-KAteIzhXqjPfLyAWBKncRO3ebUReQ=="
    bucket = "messungen"#os.environ['DOCKER_INFLUXDB_INIT_BUCKET']
    org = "dev"#os.environ['DOCKER_INFLUXDB_INIT_ORG']
else:
    
    token = os.environ['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']
    bucket = os.environ['DOCKER_INFLUXDB_INIT_BUCKET']
    org = os.environ['DOCKER_INFLUXDB_INIT_ORG']

    

print(token)
client = InfluxDBClient(url="http://InfluxDB:8086", token=token)

# You can generate a Token from the "Tokens Tab" in the UI


def add_temperature(tabelname: str, tag: int, temperature: float, humidity: float, temperature2: float):

    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point(tabelname)\
        .tag("nodeid", tag)\
        .field("temperature", temperature)\
        .field("humidity", humidity)\
        .field("temperature2", temperature2)
    write_api.write(bucket, org, point)
    print("geschrieben")
    
    return True


def get_mesuremnt():
    
    query = f'from(bucket: "mybucket") |> range(start: 0, stop: now())|> sort(columns: ["_time"], desc: false) |> last(column: "_time")'
    tables = client.query_api().query(query, org=org)
    result={}
    for table in tables:
     for row in table.records:
        
        values = row.values
        print(values)
        nodeid = values['nodeid']
        if not nodeid in result:
            result [nodeid] = {'nodeid': int(nodeid)}
        result[nodeid][values['_field']]=values['_value']   
    

    print(result)
    return result
    
