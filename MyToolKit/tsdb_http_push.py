#!/usr/bin/env python
'''
Author: Veerendra.K
Description: An example snippet code which pushes the metrics OpenTSDB by HTTP REST API

Refer: http://opentsdb.net/docs/build/html/api_http/index.html 
Know how to setup HTTPS proxy for this: https://networkhop.wordpress.com/2017/02/28/how-to-create-https-proxy-in-apache/#more-868
'''
import os
import requests
import time
import json

hostname=os.uname()[1]
url="https://localhost:8443/api/put"
headers = {'content-type': 'application/json'}

time=int(time.time())

data={
    "metric": "cpu.util",
    "timestamp": time,
    "value": 18, # <-- Get the CPU here
    "tags": {
       "host": hostname
    }
}

json_data=json.dumps(data)
print json_data
response = requests.post(url, data=json_data,headers=headers, verify=False)
print response
