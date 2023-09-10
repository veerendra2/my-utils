#!/usr/bin/env python
"""
Author: Veerendra K
Description: Displays near wifi hotspots
"""
import subprocess
import os
import json
import re
import argparse

wireless_file="/proc/net/wireless"
re_compile_patterns1={"MAC Address" : 'Address:(.*)',
                    "Channel"       : 'Channel:(.*)',
                    "Frequency"     : 'Frequency:(.\S+ .\S+)',
                    "Encryption"    : 'Encryption key:(.*)',
                    "Mode"          : 'Mode:(.*)',
                    "Quality"       : 'Quality=(.\S+)',
                    "ESSID"         : 'ESSID:(.*)',
                    "Singal Level"  : 'Signal level=(.*)',
                    "ID"            : '(.*) - Address'}

re_compile_patterns2={"Encryption Algorithm WPA" : 'IE: WPA(.*)',
                    "Encryption Algorithm"       : 'IE: IEEE(.*)',
                    "Group Cipher"               : 'Group Cipher :(.*)',
                    "Pairwise Ciphers"           : 'Pairwise Ciphers(.*)',
                    "Authentication Suites"      : 'Authentication Suites(.*)'}

def get_ap_results(iface):
    result=None
    ap=dict()
    for x in range(3):
        if x==2:
            print "iwlist is not working?"
            exit(1)
        try:
            return subprocess.check_output("iwlist {} s".format(iface),shell=True)
            break
        except:
            continue

def find_iface():
    try:
        with open(wireless_file) as f:
            return re.findall(r'(.*):',f.read())[0].strip()
    except:
        while 1:
            iface=raw_input("\nWireless interface not found.\nPlease enter wireless interface name> ").strip()
            if iface:
                return iface

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Displays wifi hotspots info near to you. [Coded by VEERENDRA KAKUMANU]')
    parser.add_argument('-j', action='store_true', dest='json_val', default=False ,help='Dumps in json format')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0')
    results=parser.parse_args()
    ssids=get_ap_results(find_iface())
    for name,pattern in re_compile_patterns1.items():
        re_compile_patterns1[name]=re.compile(pattern)
    for names,pattern in re_compile_patterns2.items():
        re_compile_patterns2[names]=re.compile(pattern)
    final_json=list()
    if not results.json_val:
        print "+".ljust(5,"-")+"+".ljust(22,"-")+"+".ljust(20,"-")+"+".ljust(10,"-")+"+".ljust(12,"-")+"+".ljust(15,"-")+"+"
        print "| ID".ljust(5," ")+"|"+"        ESSID        |"+"    MAC Address    |"+" Channel |"+" Frequency |"+" Singal Level |"
        print "+".ljust(5,"-")+"+".ljust(22,"-")+"+".ljust(20,"-")+"+".ljust(10,"-")+"+".ljust(12,"-")+"+".ljust(15,"-")+"+"
    for line in ssids.split("Cell"):
        if line and "Scan completed" not in line:
            wifi_json=dict()
            for names,objects in re_compile_patterns1.items():
                wifi_json.setdefault(names,objects.findall(line)[0].strip().strip('"'))
            if not results.json_val:
                print "|",wifi_json["ID"].ljust(3," ")+"|",wifi_json["ESSID"].ljust(20," ")+"|",wifi_json["MAC Address"].ljust(18," ")+"|",wifi_json["Channel"].ljust(8," ")+"|",wifi_json["Frequency"].ljust(10," ")+"|",wifi_json["Singal Level"].ljust(13," ")+"|"
            for names,objects in re_compile_patterns2.items():
                try:
                    wifi_json.setdefault(names,objects.findall(line)[0].strip())
                except: pass
            final_json.append(wifi_json)
    if not results.json_val:
        print "+".ljust(5,"-")+"+".ljust(22,"-")+"+".ljust(20,"-")+"+".ljust(10,"-")+"+".ljust(12,"-")+"+".ljust(15,"-")+"+"
    else:
        print json.dumps(final_json)
