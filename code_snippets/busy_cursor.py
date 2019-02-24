#!/usr/bin/env python
'''
Author: Veerendra.K
Description: An example 'Busy Cursor' snippet
'''
import sys
import time

print "processing...\\",
syms = ['\\', '|', '/', '-']
bs = '\b'

for _ in range(100):
    for sym in syms:
        sys.stdout.write("\b%s" % sym)
        sys.stdout.flush()
        time.sleep(.01)
print ""
