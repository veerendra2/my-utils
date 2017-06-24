#!/usr/bin/envn python
'''
Author: Veerendra Kakumanu
Description: Simple Do Not Distrube(DND) script, tempararly blocks the specified site in localhost.
NOTE: After running the dnd.py, restart broswer to get chages
'''
import os
import argparse

host_file="/etc/hosts"
block_sites_list=["www.facebook.com",
                    "login.facebook.com",
                    "www.login.facebook.com",
                    "fbcdn.net",
                    "www.fbcdn.net",
                    "fbcdn.com",
                    "www.fbcdn.com",
                    "static.ak.fbcdn.net",
                    "static.ak.connect.facebook.com",
                    "connect.facebook.net",
                    "www.connect.facebook.net",
                    "apps.facebook.com",
                    "www.youtube.com"
                  ]

def dndON():
    with open(host_file,"a+") as f:
        content=f.read()
        for site in block_sites_list:
            if site not in content:
                f.write("127.0.0.1\t{}\n".format(site))
                f.write("::1\t{}\n".format(site))
def dndOFF():
    final_content=list()
    with open(host_file,"a+") as f:
        for line in f.readlines():
            try:
                site=line.split()[1]
            except: continue
            if site not in block_sites_list:
                final_content.append(line)
        f.seek(0)
        f.truncate()
        f.writelines(final_content)

if __name__=='__main__':
    if not os.geteuid()==0:
        print "Please run the script as sudo"
        exit()
    arg=argparse.ArgumentParser(description="Do Not Distrube")
    arg.add_argument("-0", action="store_true", dest="off", default=False, help="DND Off")
    arg.add_argument("-1", action="store_true", dest="on", default=False, help="DND On")
    arg.add_argument("-v", action="version",version='%(prog)s 0.1')
    result=arg.parse_args()
    if result.on:
        dndON()
    elif result.off:
        dndOFF()
    else:
        print "Check help with `sudo dnd.py -h"
