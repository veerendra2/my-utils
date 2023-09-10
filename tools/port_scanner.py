#!/usr/bin/env python
'''
Author: Veerendra K
Description: nmap like utility, which gets open ports in localhost
'''
import socket
import subprocess
import sys
import time
from datetime import datetime
t1=time.time()
try:
    for port in range(1,65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
	socket.setdefaulttimeout(0.01)
        if result == 0:
            print port
except:
	print "Socker Error!"
t2=time.time()
print "Delay=>",tin(t2-t1)
