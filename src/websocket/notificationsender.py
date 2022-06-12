import requests
import json


def sendnotifcation():
    notedata = {
        'appId': '2917',
        'appToken': 'fwbJ1bWEA3jg6f7LsxMdLQ',
        'title': 'Alarm!',
        'body': 'Alarm at setction'
    }
    
    headers = {'Content-Type': 'application/json'}
    s = json.dumps(notedata)
    url ='https://app.nativenotify.com/api/notification'

    r = requests.post( url, headers=headers, data=s)



