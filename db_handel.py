from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
def add_tempetratur(tabelname:str,tag:str,temp:float,humidity:float,SingleDS18B20:float): 
 token = "4k6hl6C_GM1r2EjVyWIJJ4muZSeHr5ufvdP761paPSukNwLv3FMLMiSGqkfg2Z4lEs-aFxFk9dF8wKj3ETxOMw=="
 bucket = "mesurement"
 org = "privat"
 client = InfluxDBClient(url="http://localhost:8086", token=token)
 write_api = client.write_api(write_options=SYNCHRONOUS)
 
 point = Point(tabelname)\
   .tag("senorid", tag)\
   .field("TEMP", temp)\
   .field("HUIM", humidity)\
   .field("SingleDS18B20",SingleDS18B20) 
 write_api.write(bucket, org, point)
 
 return True






