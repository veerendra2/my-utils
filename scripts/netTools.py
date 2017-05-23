#!/usr/bin/env python
'''
Author: Veerendra. Kakumanu
Description: Simple "Domain Tools" script: Displays specified host info, your ISP info 
'''
import json
import urllib2
import argparse

WHO_IS="http://ip-api.com/json/"
MY_PUBLIC_IP="http://whatismyip.akamai.com/"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getData(url):
    try:
        res=urllib2.urlopen(url)
    except:
        print Colors.FAIL+"Something went wrong. Check your Internet connection?"+Colors.ENDC
        exit()
    if res.getcode()==200:
        return res
    else:
        print Colors.FAIL+"HTTP Error "+res.getcode()+Colors.ENDC
        exit()

def getDomainInfo(who=None):
    if who:
        url=WHO_IS+who
        ip_label="IP Address"
    else:
        url=WHO_IS
        ip_label="Your Public IP"
    res=getData(url)
    dictionary=json.loads(res.read())
    print "+".ljust(59,"-")+"+"
    print "| Host".ljust(17),dictionary["org"].ljust(40," "),"|"
    print "| "+ip_label.ljust(15),dictionary['query'].ljust(40," "),"|"
    print "| ISP".ljust(17),dictionary['isp'].ljust(40," "),"|"
    print "| AS".ljust(17),dictionary['as'].ljust(40," "),"|"
    print "| City".ljust(17),dictionary['city'].ljust(40," "),"|"
    print "| Region".ljust(17),dictionary['regionName'].ljust(40," "),"|"
    print "| Country".ljust(17),dictionary['country'].ljust(40," "),"|"
    print "| Latitude".ljust(17),str(dictionary['lat']).ljust(40," "),"|"
    print "| Longitude".ljust(17),str(dictionary['lon']).ljust(40," "),"|"
    print "| Time Zone".ljust(17),str(dictionary['timezone']).ljust(40," "),"|"
    print "| ZIP".ljust(17),str(dictionary['zip']).ljust(40," "),"|"
    print "+".ljust(59,"-")+"+"

def getPublicIp():
    res=getData(MY_PUBLIC_IP)
    print Colors.BOLD+Colors.OKGREEN+"YOUR PUBLIC IP ADDRESS:",str(res.read())+Colors.ENDC

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Net Tools')
    parser.add_argument('-m', action='store_true', dest='myip', default=False ,help='shows public IP')
    parser.add_argument('-H', action='store', dest='host',help='shows domain info of the host')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0')
    results = parser.parse_args()
    if results.myip:
        getPublicIp()
    elif results.host:
        getDomainInfo(results.host)
    else:
        getDomainInfo()
