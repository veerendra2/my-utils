#!/usr/bin/env python2
'''
Author : Veerendra K
Description : Sends data to pastebin.com
Docs : https://pastebin.com/api
'''

import requests
import argparse
import time
import xml.etree.ElementTree as ET
import sys
import os
import warnings

warnings.filterwarnings("ignore")
API_URL = "https://pastebin.com/api/api_post.php"
API_KEY = ""

if not API_KEY:
    print "[!] Missing API key. Get API key from your account(https://pastebin.com/api#1) and specify in code"
    exit(1)


def create_paste(text, visiblity, pformat=None, pname=None):
    if not pname:
        pname = "API Paste-" + str(time.time())
    payload = {"api_dev_key": API_KEY, "api_option": "paste",
               "api_paste_code": text, "api_paste_private": visiblity,
               "api_paste_name": pname}
    if pformat:
        payload.setdefault("api_paste_format", pformat)
    try:
        response = requests.post(API_URL, data=payload)
        print response.text
    except:
        print "[!] Something went wrong! Please try again"
        exit(1)


def list_trending_paste():
    payload = {"api_dev_key": API_KEY, "api_option": "trends"}
    try:
        response = requests.post(API_URL, payload)
        xml_data = "<list>" + response.text.encode("utf-8") + "</list>"
        tree = ET.ElementTree(ET.fromstring(xml_data))
        print "********** TRENDING PASTEBIN **********"
        for items in tree.getroot():
            print items[8].text.ljust(35, " "),items[2].text
    except:
        print "[!] Something went wrong! Please try again"
        exit(1)


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Sends data to pastebin.com\n[*]PIPE the ouput to the script.\
                                \nExample: echo 'Test' | python pastebin.py", formatter_class=argparse.RawTextHelpFormatter)
    parse.add_argument("-t", dest="trend", action="store_true", default=False, help="Gets trending paste")
    parse.add_argument("-p", dest="public", action="store_true", default=False, help="Public Paste")
    parse.add_argument("-f", dest="pformat", action="store",
                       help="Format of the text(Optional). Please refer formats https://pastebin.com/api#5")
    parse.add_argument("-n", dest="pname", action="store", help="Name of the past(Optional)")
    options = parse.parse_args()
    if not os.isatty(0):
        private = 2
        if options.public:
            private = 1
        text = sys.stdin.read().strip()
        create_paste(text, private, options.pformat, options.pname)
    else:
        if not options.pformat or not options.pname or not options.public:
            if options.trend:
                list_trending_paste()
            else:
                print "[!] Please check the help: 'python pastebin.py -h'"
        else:
            print "[!]Options '-p', '-f' and '-n' should only used while creating paste\
            \nPlease check help with 'python pastebin.py -h'"
