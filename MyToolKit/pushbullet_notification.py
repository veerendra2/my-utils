#!/usr/env python
'''
Author : Veerendra Kakumanu
Description : Sends "pushbullet" notification to Device / Channel
Docs : https://docs.pushbullet.com/
'''
import json
import requests


def send_notification(title, body, channel=False):
    import random
    personal_greetings = ["Sir, ", "Boss, ", "Mr. Veerendra, "]
    crowed_greetings = ["Ok People", "Hello there"]
    api_key = "o.Wp7IYNaO0ftCGRNplyAA5juwRQKGLQ7aZVXy0"  # Fake API KEY
    push_api = "https://api.pushbullet.com/v2/pushes"
    my_device_id = "ujv5wTYow0asjAw1gGLQ7a"  # Fake Device ID
    if channel:
        title = random.choice(crowed_greetings) + "It is regarding " + title
        data = {"type": "note", "title": title,
                "body": body, "channel_tag": "omega"}
    else:
        title = random.choice(personal_greetings) + "It is regarding " + title
        data = {"type": "note", "title": title,
                "body": body}
    headers = {"Content-Type": "application/json", "Access-Token": api_key}
    res = requests.post(push_api, data=json.dumps(data), headers=headers)
    print res

if __name__ == "__main__":
    '''
    Do any long running task...and send notification about that task
    '''
    send_notification("Test", "This is test message!")
