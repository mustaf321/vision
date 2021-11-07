from pymongo import MongoClient

client=MongoClient(
    'mongodb://localhost:27017/'
)


db=client.visiondb
alarms=db.alarms
nodes=db.nodes



def list_alarms():
    results =[]
    print(db)
    for result in alarms.find({},{"_id":0}):
        print(result)
        results.append(result)
    print(results)
    return results


def add_alarm(nodeid, range):
    print(db)
    node_exists = nodes.find_one({"nodeid": nodeid})
    print(node_exists)
    if node_exists is not None:
        alarms.update({"nodeid":nodeid},{"nodeid": nodeid, "range":range.dict()},upsert=True)
        return True
    else:
     return False
    

def get_alarm(nodeid):
    result = alarms.find_one({"nodeid":nodeid}, {"_id":0})
    return result


def delete_alarm(nodeid):
    result = alarms.delete_one({"nodeid":nodeid})
    return result.deleted_count == 1


def list_nodes():
    results =[] 
    for result in nodes.find({},{"_id":0}):
     results.append(result)
    print(results)
    return results


def add_node(nodeid, details):
    if nodes.find_one({"nodeid":nodeid}):
        return True
    else:
        nodes.insert({"nodeid":nodeid, "details":details.dict()})
        return False
    

def get_node(nodeid):
    result = nodes.find_one({"nodeid":nodeid}, {"_id":0})
    return result


def delete_node(nodeid):
    result = nodes.delete_one({"nodeid":nodeid})
    return result.deleted_count == 1    