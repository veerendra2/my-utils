#!/usr/bin/env python
'''
Author: Veerndra.K
Description: A simple example snippet, sends metrics to OpenTSDB
Requried Modules: potsdb (pip install potsdb)
'''
import potsdb
import time

tsdbIp="127.0.0.1"
tsdbPort=4343
interval=5
try :
    metrics = potsdb.Client(tsdbIp,tsdbPort,qsize=1000, host_tag=True, mps=100, check_host=True)
    ts = int(time.time())
    metrics.send("sample.test",1,host="my-host")
    print "sample.test 1 host=my-host"
    metrics.wait()
except:
    pass
