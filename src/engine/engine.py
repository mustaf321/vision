from websocket.broadcaster import broadcast_new_alarm, broadcast_new_node
from db.dbmanegment_handel import list_alarms, add_alarm, get_alarm, delete_alarm,add_node,list_nodes



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
    x = add_alarm(nodeid,range)
    if x :
     await broadcast_new_alarm(nodeid,range)
     return True
    else:
     return False



async def received_new_node(nodeid):
    print("Received new node")
    print(nodeid)
    if add_node(nodeid):
     await broadcast_new_node(nodeid)
     return True
    else:
     return False
