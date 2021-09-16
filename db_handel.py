from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
token = "xl_5uteTN5MNikM6nWXBFfzXLRGmAwBl9QP3AcBSDYjbbOvtZGFj28cKUJM45phmB5HoMo83bOtOe1i1fbatjw=="
bucket = "messungen"
org = "dev"
client = InfluxDBClient(url="http://localhost:8086", token=token)
 
# You can generate a Token from the "Tokens Tab" in the UI
def add_tempetratur(tabelname:str,tag:str,temp:float,humidity:float,SingleDS18B20:float): 

 
 write_api = client.write_api(write_options=SYNCHRONOUS)
 
 point = Point(tabelname)\
   .tag("senorid", tag)\
   .field("TEMP", temp)\
   .field("HUIM", humidity)\
   .field("SingleDS18B20",SingleDS18B20) 
 write_api.write(bucket, org, point)
 
 return True


def get_mesuremnt():
 query = f'''from(bucket: "messungen") |> range(start: -1h)  |> filter(fn: (r) => r["_measurement"] == "mesungen")
 |> last()
  |> filter(fn: (r) => r["_field"] == "SingleDS18B20" or r["_field"] == "TEMP" or r["_field"] == "HUIM") '''
 result = client.query_api().query(query, org=org)

 results = []
 
 for table in result:
  for record in table.records:
    results.append((record.get_field(), record.get_value()))
  
 print(len(results))  
 return results


