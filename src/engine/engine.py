from websocket.broadcaster import broadcast_new_alarm
from db.dbmanegment_handel import list_alarms, add_alarm, get_alarm, delete_alarm



#only for delay
import time


def get_all_alarms():
    #only for showing cirle
    time.sleep(2)
    return list_alarms()


async def received_new_alarm(nodeid,range):
    print("Received new Alarm")
    print(nodeid)
    print(range)
    if add_alarm(nodeid,range):
     await broadcast_new_alarm(nodeid,range)
     return True
    else:
     return False
