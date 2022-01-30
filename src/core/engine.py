

from websocket.broadcaster import broadcast_new_alarm, broadcast_new_node
from db.dbmanegment_handel import list_alarms, add_alarm, list_alarm, delete_alarm, add_node, list_nodes, delete_node, list_node
from db.db_handel import get_mesuremnt,add_tempetratur
from pydantic import BaseModel, ValidationError
# only for delay
import time

class Alarm(BaseModel):
    nodeid:int
    min : float
    max : float
    status: bool



def get_all_alarms():
    # only for showing cirle
    time.sleep(2)
    return list_alarms()


def get_alarm(nodeid):
    time.sleep(2)
    return list_alarm(nodeid)


async def remove_alarm(nodeid):
    x = delete_alarm(nodeid)
    if x:
        return True
    else:
        return False

def defuse_alarm(nodeid):
    x=get_alarm(nodeid)
    if x:
        x['status']=False
        a = Alarm.parse_obj(x)
        return add_alarm(a)
    else:
        return False

async def received_new_alarm(alarm):
    print("Received new Alarm")
    print(alarm.nodeid)
    x = add_alarm(alarm)
    if x:
        await broadcast_new_alarm(alarm)
        return True
    else:
        return False

def add_measurement(nodeid, measurement):
  k = add_tempetratur("mesungen",nodeid,measurement.temperature,measurement.humidity,measurement.SingleDS18B20)
  monitoring()

def get_all_measurements():
    return get_mesuremnt()


def  delete_influx_measurement(measurment_id):
  return True

def monitoring():
    mesurements = get_mesuremnt()
    alarms = get_all_alarms()
    print(measurements)

    for mesurement in mesurements:
        mesurement_index = mesurements.get(mesurement)
        print(mesurement_index) 
        print("+++")
        print(alarms)
        print("+++++++++++")
        print(mesurement)
        alarm_index = alarms[int(mesurement)-1]

        print(alarm_index)
       

        mesurement_nodeid = int(mesurement_index.get('nodeid'))
        alarm_nodeid = alarm_index.get('nodeid')
        if mesurement_nodeid is alarm_nodeid:
            temp1 = mesurement_index.get('TEMP')
            hum = mesurement_index.get('HUM')
            temp2 = mesurement_index.get('SingleDS18B20')
            temp=(temp1 +temp2) /2
            alarm_max = alarm_index.get('max')
            alarm_min = alarm_index.get('min')
            if temp > alarm_max or temp < alarm_min:
                  alarm_index['status']=True
                  a = Alarm.parse_obj(alarm_index) 
                  add_alarm(a)
                  broadcast_new_alarm(a)
                 


async def received_new_node(nodeid):
    print("Received new node")
    print(nodeid)
    if add_node(nodeid):
        await broadcast_new_node(nodeid)
        return True
    else:
        return False


def get_all_nodes():
    time.sleep(2)
    return list_nodes()


def get_node(nodeid):
    time.sleep(2)
    return list_node(nodeid)


def remove_node(nodeid):
    time.sleep(2)
    return delete_node(nodeid)
