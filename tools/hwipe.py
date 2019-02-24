#!/usr/bin/env python2
'''
Author: Veerendra Kakumanu
Description: Wipes commands history in terminal for every user including root. Requires sudo
'''
import os
import grp
import pwd


def set_owner(username, path):
    uid = pwd.getpwnam(username).pw_uid
    gid = grp.getgrnam(username).gr_gid
    os.chown(path, uid, gid)
    os.chmod(path, 0755)


def secure_delete(path, passes=1):
    with open(path, "a+") as delfile:
        length = delfile.tell()
        for i in range(passes):
            delfile.seek(0)
            delfile.write(os.urandom(length))
    os.remove(path)
    open(path, "w").close()


for user in os.listdir("/home"):
    if os.path.isdir("/home/"+user):
        path = "/home/"+user+"/.bash_history"
        if os.path.exists(path):
            secure_delete(path, 2)
        set_owner(user, path)
if os.path.exists("/root/.bash_history"):
    secure_delete("/root/.bash_history", 2)
    set_owner("root", "/root/.bash_history")


