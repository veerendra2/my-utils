#!/usr/bin/env python
'''
Author: Veerendra.K
Description: 'netstat' like tool. Retrieves connection details of pid. Reads info from /proc/net/tcp/ /proc/[pid]/fd/
'''
import os
import socket
import struct
import sys

states={
"01":"TCP_ESTAB",
"02":"TCP_SYN_SENT",
"03":"TCP_SYN_RECV",
"04":"TCP_FIN_WAIT1",
"05":"TCP_FIN_WAIT2",
"06":"TCP_TIME_WAIT",
"07":"TCP_CLOSE",
"08":"TCP_CLOSE_WAIT",
"09":"TCP_LAST_ACK",
"0A":"TCP_LISTEN",
"0B":"TCP_CLOSING",
"0C":"TCP_MAX_STATES"
}

def parseTCPLine(line,pid):
    if line:
        part=line.split()
        src_ip=socket.inet_ntoa(struct.pack("<L",int(part[1].split(":")[0],16)))
        src_port=str(int(part[1].split(":")[1],16))
        dst_ip=socket.inet_ntoa(struct.pack("<L",int(part[2].split(":")[0],16)))
        dst_port=str(int(part[2].split(":")[1],16))
        print pid.ljust(5," "),src_ip.ljust(14," "),src_port.ljust(14," "),states[part[3].strip()].ljust(18," "),dst_ip.ljust(18," "),dst_port

def getSockets(pid):
    inodes=dict()
    fd_path=os.path.join("/proc/",pid,"fd")
    if os.path.exists(fd_path):
        for fd in os.listdir(fd_path):
            try:
                f=os.readlink(os.path.join(fd_path,fd))
            except:pass
            if "socket:" in f:
                inodes.setdefault(f.split("[")[1].split("]")[0], pid)
    else:
        print pid,"not found"
    return inodes

def readTCPFile(inodes):
    with open("/proc/net/tcp") as f:
        for line in f.readlines():
            for node,pid in inodes.items():
                if node in line:
                    parseTCPLine(line,pid)

def header():
    print "PID".ljust(5," "),"Source IP".ljust(13," "),"Source Port".ljust(16," "),"State".ljust(16," "),"Destination IP".ljust(15," "),"Destination Port"
    print "".ljust(88,"-")

if __name__=="__main__":
    if len(sys.argv)>1:
        header()
        for pid in sys.argv[1:]:
            if pid.isdigit():
                readTCPFile(getSockets(pid))
    else:
        header()
        for dir in os.listdir("/proc"):
            if dir.isdigit():
                readTCPFile(getSockets(dir))

