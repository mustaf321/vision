from time import sleep
import requests
from threading import Timer
import random
run = True
inti_temperature = random.randrange(1, 20, 1)
init_humidity = random.randrange(10, 40, 1)
init_SingleDS18B20 = random.randrange(1, 20, 1)
init_pload = {'nodeid': 1, "temperature": inti_temperature,
         'humidity': init_humidity, 'SingleDS18B20': init_SingleDS18B20}

requests.post('http://192.168.2.124:8080/api/v1/temperatures/1', data=init_pload)


def test():
    global run
    temperature = random.randrange(1, 20, 1)
    humidity = random.randrange(10, 40, 1)
    SingleDS18B20 = random.randrange(1, 20, 1)
    pload = {'nodeid': 1, "temperature": temperature,
             'humidity': humidity, 'SingleDS18B20': SingleDS18B20}
    wr = requests.put(
        'http://192.168.2.124:8080/api/v1/temperatures/1', data=pload)
    print(wr.status_code)
    print(wr.headers)
    
    if run:
        Timer(5, test).start()


test()
