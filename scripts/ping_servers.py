'''
Author: Veerendra K
Description: Pings to specified servers with multi threading
'''
import threading
import subprocess
import time
import logging
from logging.handlers import RotatingFileHandler

lock = threading.Lock()
poll_time = 30

IPS = ["192.100.0.4", "192.100.0.6",
    "192.100.0.7", "192.100.0.16",
    "192.100.0.17", "192.100.0.25",
    "192.100.0.26", "192.100.0.8",
    "192.100.0.9", "192.100.0.10",
    "192.100.0.11", "192.100.0.12",
    "192.100.0.13", "192.100.0.14",
    "192.100.0.15", "192.100.0.18",
    "192.100.0.19", "192.100.0.20",
    "192.100.0.21", "192.100.0.22",
    "192.100.0.23", "192.100.0.27",
    "192.100.0.28"]
#IPS = ["172.0.0.1", "172.0.0.2"]

import logging
from logging.handlers import RotatingFileHandler

LOG_LOCATION = 'ping_server.log'
MAX_SIZE_LOG=2000 #Mega Bytes
BACKUP_COUNT=1

handler=RotatingFileHandler(LOG_LOCATION, mode='a', maxBytes=MAX_SIZE_LOG*1024*1024, backupCount=BACKUP_COUNT, encoding=None, delay=0)
handler.setFormatter(logging.Formatter('%(asctime)s' + ' - %(message)s'))
log=logging.getLogger()
levels={"debug":logging.DEBUG,
        "info":logging.INFO,
        "warning":logging.WARNING,
        "error":logging.ERROR,
        "critical":logging.CRITICAL}

def log_it(level,message):
    log.setLevel(levels[level])
    log.addHandler(handler)
    handler.setLevel(levels[level])
    if level=="info":
        log.info(message)
    elif level=="debug":
        log.debug(message)
    elif level=="warning":
        log.warning(message)
    elif level=="error":
        log.error(message)
    elif level=="critical":
        log.critical(message)


def execute(cmd):
    """
    :param cmd: Command to execute
    :param verbose: Be verbose
    :return: On success, it return command output. On failure, it returns 1
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = []
    while True:
        line = p.stdout.readline()
        out.append(line)
        if not line and p.poll() is not None:
            break
    return ''.join(out).strip()

def ping(ip):
    while True:
        try:
            cmd = "ping -n -c 1 {}".format(ip)
            ping_ouput = execute(cmd)
            first_line = ping_ouput.split('\n')[1]
            if not first_line:
                first_line = ping_ouput.split('\n')[-1]
            lock.acquire()
            log_it("debug","{}: {}".format(ip, first_line))
            lock.release()
            time.sleep(poll_time)
        except KeyboardInterrupt:
            print "[-] Received KeyboardInterrupt. Quitting."
            exit(1)

if __name__ == '__main__':
    print "[*] Staring {} Threads at {}".format(len(IPS), time.strftime("%d/%m/%Y %H:%M:%S"))
    print "[*] Log Location: ping_server.log"
    try:
        threads = [threading.Thread(target = ping, args=(ip,)) for ip in IPS]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
#        while True:
#            time.sleep(100)
    except KeyboardInterrupt:
        print "[-] Received KeyboardInterrupt. Quitting."
        exit(1)
