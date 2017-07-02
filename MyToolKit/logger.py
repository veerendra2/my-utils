#!/usr/bin/env python
'''
Author: Veerendra.Kakumanu
Description: A simple logger snippet, usefull to log info to log file. Just paste the code and call 'log_it()' with arguments 'level' & 'info'
'''
import logging
from logging.handlers import RotatingFileHandler

LOG_LOCATION = '/var/log/script.log'
MAX_SIZE_LOG=20 #Mega Bytes
BACKUP_COUNT=0

handler=RotatingFileHandler(LOG_LOCATION, mode='a', maxBytes=MAX_SIZE_LOG*1024*1024, backupCount=BACKUP_COUNT, encoding=None, delay=0)
handler.setFormatter(logging.Formatter('%(asctime)s %(name)s[%(process)d] %(levelname)s: %(message)s'))
log=logging.getLogger('YOUR-SCRIPT')
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

log_it("critical","Something happened!")
