#!/usr/bin/env python
'''
Author: Veerendra.K
Description: Simple "Domain Tools" like tools, displays specified host info & your public IP inof
'''
import json
import urllib2
import argparse

WHO_IS="https://ipv4.ipleak.net/json/"
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
    else:
        url=WHO_IS
    res=getData(url)
    dictionary=json.load(res)
    if "ips" in dictionary:
        print "Host".ljust(6)+": "+dictionary["query_text"]
        if len(dictionary["ips"])>1: print Colors.OKBLUE+"*This host has multiple IPs. Below are the some IPs"+Colors.ENDC
        for ips, info in dictionary["ips"].items():
            print "+".ljust(53,"-")+"+"
            print "| IP Address".ljust(15),ips.ljust(36," "),"|"
            print "| City".ljust(15),str(info["city_name"]).ljust(36," "),"|"
            print "| Region".ljust(15),str(info["region_name"]).ljust(36," "),"|"
            print "| Country".ljust(15),str(info["country_name"]).ljust(36," "),"|"
            print "| Continent".ljust(15),str(info["continent_name"]).ljust(36," "),"|"
            print "| Latitude".ljust(15),str(info["latitude"]).ljust(36," "),"|"
            print "| Longitude".ljust(15),str(info["longitude"]).ljust(36," "),"|"
            print "| Time Zone".ljust(15),str(info["time_zone"]).ljust(36," "),"|"
        print "+".ljust(53,"-")+"+"
    else:
        print "+".ljust(57,"-")+"+"
        if who:
            print "| IP Address".ljust(17),str(dictionary["ip"]).ljust(38," "),"|"
        else:
            print "| Your Public IP".ljust(17),str(dictionary["ip"]).ljust(38," "),"|"
        print "| City".ljust(17),str(dictionary["city_name"]).ljust(38," "),"|"
        print "| Region".ljust(17),str(dictionary["region_name"]).ljust(38," "),"|"
        print "| Country".ljust(17),str(dictionary["country_name"]).ljust(38," "),"|"
        if "continent_name" in dictionary:
            print "| Continent".ljust(17),str(dictionary["continent_name"]).ljust(38," "),"|"
        if "isp_name" in dictionary:
            print "| ISP Name".ljust(17),str(dictionary["isp_name"]).ljust(38," "),"|"
        if "organization_name" in dictionary:
            print "| Org. Name".ljust(17),str(dictionary["organization_name"]).ljust(38," "),"|"
        if "domain" in dictionary:
            print "| Domain".ljust(17),str(dictionary["domain"]).ljust(38," "),"|"
        if "as_number" in dictionary:
            print "| AS Number".ljust(17),str(dictionary["as_number"].split()[0]).ljust(38," "),"|"
        if "netspeed" in dictionary:
            print "| Net Speed".ljust(17),str(dictionary["netspeed"]).ljust(38," "),"|"
        if "user_type" in dictionary:
            print "| User Type".ljust(17),str(dictionary["user_type"]).ljust(38," "),"|"
        print "| Latitude".ljust(17),str(dictionary["latitude"]).ljust(38," "),"|"
        print "| Longitude".ljust(17),str(dictionary["longitude"]).ljust(38," "),"|"
        print "| Time Zone".ljust(17),str(dictionary["time_zone"]).ljust(38," "),"|"
        print "+".ljust(57,"-")+"+"


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
