from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "xl_5uteTN5MNikM6nWXBFfzXLRGmAwBl9QP3AcBSDYjbbOvtZGFj28cKUJM45phmB5HoMo83bOtOe1i1fbatjw=="
org = "dev"
bucket = "messungen"

client = InfluxDBClient(url="http://localhost:8086", token=token)






query = f'from(bucket: "messungen") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "mesungen")|> filter(fn: (r) => r["_field"] == "TEMP") '
result = client.query_api().query(query, org=org)

results = []
for table in result:
  for record in table.records:
    results.append((record.get_field(), record.get_value()))


print(results[0])
