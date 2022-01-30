from datetime import datetime
import json
from fastapi.params import Query
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
token = "JgB6MmgiBryVOP08dEoopf-mPMODImlmHmekmoYZWzDA98HTX5GdgvC2Ay01utjPddK99claY-VcAHy2OQfgUw=="
bucket = "messungen"
org = "dev"
client = InfluxDBClient(url="http://localhost:8086", token=token)

# You can generate a Token from the "Tokens Tab" in the UI


def add_tempetratur(tabelname: str, tag: int, temp: float, humidity: float, SingleDS18B20: float):

    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point(tabelname)\
        .tag("nodeid", tag)\
        .field("TEMP", temp)\
        .field("HUIM", humidity)\
        .field("SingleDS18B20", SingleDS18B20)
    write_api.write(bucket, org, point)

    return True


def get_mesuremnt():
    query = f'from(bucket: "messungen") |> range(start: 0, stop: now())|> sort(columns: ["_time"], desc: false) |> last(column: "_time")'
    tables = client.query_api().query(query, org=org)
    result={}
    for table in tables:
     for row in table.records:
        
        values = row.values
        print(values)
        nodeid = values['nodeid']
        if not nodeid in result:
            result [nodeid] = {'nodeid': nodeid}
        result[nodeid][values['_field']]=values['_value']   
    return result
