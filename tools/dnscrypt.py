#!/usr/bin/env python
'''
Author: Veerendra. Kakumanu
Description: An automated DNSCrypt Proxy creator using 'dnscrypt-proxy'

Required Packages: dnscrypt-proxy
Motivation: Read https://www.opendns.com/about/innovations/dnscrypt/
'dnscrypt-proxy' Installation Guide: http://www.webupd8.org/2014/08/encrypt-dns-traffic-in-ubuntu-with.html
'''
import csv
import urllib
import os
import argparse

PID_FILE_LOCATION="/var/run/dnscrypt-proxy.pid"
LOG_FILE_LOCATION="/var/log/dnscrypt-proxy.log"
SERVERS_LIST_FILE="/opt/dnscrypt-resolvers.csv"


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def download_csv():
    servers_dict = dict()
    global SERVERS_LIST_FILE
    print Colors.OKBLUE+"Downloading Latest 'dnscrypt-resolvers.csv'.."+Colors.ENDC
    try:
        csv_file = urllib.URLopener()
        csv_file.retrieve("https://raw.githubusercontent.com/jedisct1/dnscrypt-proxy/master/dnscrypt-resolvers.csv", "/opt/dnscrypt-resolvers.csv")
    except:
        print Colors.WARNING+"Unable to download 'dnscrypt-resolvers.csv'. Using default /usr/share/dnscrypt-proxy/dnscrypt-resolvers.csv"+Colors.ENDC
        if os.path.exists("/usr/share/dnscrypt-proxy/dnscrypt-resolvers.csv"):
            SERVERS_LIST_FILE="/usr/share/dnscrypt-proxy/dnscrypt-resolvers.csv"
        else:
            print Colors.FAIL+"Default csv file not found. Exiting.."+Colors.ENDC
            exit(2)
    with open(SERVERS_LIST_FILE) as f:
        data = list(csv.reader(f, delimiter=",", quotechar='"', skipinitialspace=True))[1:]
        print "Index".ljust(5, " "), "Name".ljust(25, " "), "Location".ljust(25, " "), "DNSSEC".ljust(8,
                                                                                                      " "), "No Log".ljust(
            7, " "), "Resolver Address".ljust(30)
        print "".ljust(100, "-")
        for rows, index in zip(data, enumerate(data)):
            servers_dict.setdefault(index[0], rows[0])
            print str(index[0]).ljust(5, " "), rows[0].ljust(25, " "), rows[3].ljust(25, " "), rows[7].ljust(8, " "), \
            rows[9].ljust(7, " "), rows[10].ljust(30, " ")
    return servers_dict


def check_dnscrypt():
    ret_status=os.system("dnscrypt-proxy --version > /dev/null 2>&1")
    if ret_status!=0:
        print Colors.FAIL+"'dnscrypt-proxy' not found. Please install\n"+Colors.ENDC
        exit(2)
    
if __name__=="__main__":
    check_dnscrypt()
    parser = argparse.ArgumentParser(description='dnscrypt-auto')
    parser.add_argument('-H', action='store', dest='host',help='Connect to this DNS server')
    parser.add_argument('-d', action='store_true', dest='download', default=False, help='Download DNS server list(/opt/dnscrypt-resolvers.csv) and display')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0')
    results = parser.parse_args()
    if results.download:
        download_csv()
        print "Downloaded "+SERVERS_LIST_FILE
        exit(0)
    if results.host:
        host=results.host
    else:
        servers_dict=download_csv()
        while True:
            res=raw_input("\nPlease select one DNS server >>")
            try:
                host=servers_dict[int(res)]
                break
            except:
                print Colors.FAIL+"Invalid input, please try again"+Colors.ENDC
                continue
    print Colors.WARNING+"\nStart DNSCrypt Proxy..."+Colors.ENDC
    return_status=0
    return_status=os.system("dnscrypt-proxy -R {} -L {} -l {} -p {} -d".format(host,SERVERS_LIST_FILE,LOG_FILE_LOCATION,PID_FILE_LOCATION))
    if return_status==0:
        print Colors.BOLD+Colors.OKGREEN+"Success!"+Colors.ENDC
        print Colors.BOLD+Colors.OKBLUE+"+ Please change DNS IP to 127.0.0.1 in your network configuration"+Colors.ENDC
        print Colors.OKBLUE+"+ To kill DNSCrypt Proxy run: kill -9 `cat {}`".format(PID_FILE_LOCATION)+Colors.ENDC
        print Colors.OKBLUE+"+ Logs {}".format(LOG_FILE_LOCATION)+Colors.ENDC
    else:
        print Colors.FAIL+"Failed to start DNSCrypt Proxy!"+Colors.ENDC
