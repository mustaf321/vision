

from websocket.broadcaster import broadcast_new_alarm, broadcast_new_node
from db.dbmanegment_handel import list_alarms, add_alarm, list_alarm, delete_alarm, add_node, list_nodes, delete_node, list_node
from db.db_handel import get_mesuremnt


# only for delay
import time


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


async def received_new_alarm(alarm):
    print("Received new Alarm")
    print(alarm.nodeid)
    x = add_alarm(alarm)
    if x:
        await broadcast_new_alarm(alarm)
        return True
    else:
        return False


def monitoring():
    mesurements = get_mesuremnt()
    alarms = get_all_alarms()

    for mesurement in mesurements:
        mesurement_index = mesurements.get(mesurement)
        alarm_index = alarms[int(mesurement)-1]

        print(alarm_index)
        print(mesurement_index)

        mesurement_nodeid = int(mesurement_index.get('nodeid'))
        alarm_nodeid = alarm_index.get('nodeid')
        if mesurement_nodeid is alarm_nodeid:
            temp = mesurement_index.get('TEMP')
            hum = mesurement_index.get('HUM')
            temp2 = mesurement_index.get('SingleDS18B20')
            alarm_max = alarm_index.get('max')
            alarm_min = alarm_index.get('min')
            if temp > alarm_max or temp < alarm_min:
                  alarm_index['staust']=True
                  print("######")
                  print(type(alarm_index))
                  print("######")
                  add_alarm(alarm_index)
                 


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
