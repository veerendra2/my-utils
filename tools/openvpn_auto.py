#!/usr/bin/env python2
'''
Author: Veerendra K
Description: A simple automated script to septup VPN with "openvpn"
'''
import subprocess
import os
import argparse

PID_FILE = "/var/run/openvpn.pid"
LOG_FILE = "/var/log/openvpn.log"
OPENVPN_CMD = "sudo openvpn --config {} --auth-user-pass {} --daemon --log-append {} --writepid {}"


def execute(cmd, verbose=True):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = []
    while True:
        line = p.stdout.readline()
        out.append(line)
        if verbose:
            print line,
        if not line and p.poll() is not None:
            break
    if p.returncode != 0:
        print p.stderr.read().strip()
        return 1
    else:
        return ''.join(out).strip()


def menu():
    config_files = dict()
    id = 0
    try:
        for files in os.listdir(OVPN_DIRECTORY):
            if files.endswith(".ovpn"):
                id = id + 1
                config_files.setdefault(id, files)
                print str(id).ljust(3, " ")+files
    except OSError:
        print "[!] Please specify .ovpn files directory and authentication text file location. Help -> sudo python openvpn_auto.py -h"
        exit(1)
    if id == 0:
        print "[!] .ovpn files not found in the location {}".format(OVPN_DIRECTORY)
        exit(1)
    while 1:
        try:
            res = int(raw_input("Please select configuration file to start VPN >> "))
            if res not in config_files:
                raise IndexError
        except KeyboardInterrupt:
            print ""
            exit(0)
        except:
            print "[!] Invalid option. Please try again"
            continue
        return os.path.join(OVPN_DIRECTORY, config_files[id])


def start_opevpn(config_location):
    if check_process(False) is not None:
        print "[!] openvpn is already running."
        exit(1)
    print "[+] Logs enabled /var/log/openvpn.log"
    print "[+] PID file location /var/log/openvpn.pid"
    print "[*] Starting openvpn.(Check status with 'python openvpn_auto.py -c')"
    execute(OPENVPN_CMD.format(config_location, AUTH_FILE_LOCATION, LOG_FILE, PID_FILE))


def check_process(verbose):
    return_code = execute("pgrep openvpn", False)
    if return_code == 1:
        print "[-] openvpn is not running."
        return None
    else:
        if verbose:
            print "[+] openvpn is running with pid {}".format(return_code)
        else:
            return return_code


def kill():
    pid = check_process(False)
    if pid is not None:
        execute("sudo kill -SIGTERM {}".format(pid), False)
    exit(0)


def checks():
    return_code1 = execute("dpkg --get-selections | grep openvpn", False)
    return_code2 = execute("dpkg --get-selections | grep network-manager-openvpn-gnome", False)
    return_code3 = execute("dpkg --get-selections | grep network-manager-openvpn", False)
    if return_code1 == 1 or return_code2 == 1 or return_code3:
        print "[!] Please install openvpn, network-manager-openvpn-gnome, network-manager-openvpn-gnome and resolvconf"
        exit(1)


if __name__ == '__main__':
    OVPN_DIRECTORY = ""
    AUTH_FILE_LOCATION = ""
    arg = argparse.ArgumentParser(description="A simple automated script to septup VPN with openvpn \
                                                [Coded by @veerendra2]")
    arg.add_argument("-k", action="store_true", dest="kill", default=False, help="Graceful killing of openvpn process")
    arg.add_argument("-c", action="store_true",  dest="check", default=False, help="Check openvpn is running or not")
    arg.add_argument("-d", action="store", dest="directory", default=False, help=".ovpn files directory")
    arg.add_argument("-a", action="store", dest="auth_file", default=False, help="OpenVPN authentication txt file \
                                                                                        location")
    options = arg.parse_args()
    if options.directory and options.auth_file:
        if os.path.exists(options.directory) and os.path.exists(options.auth_file):
            OVPN_DIRECTORY = options.directory
            AUTH_FILE_LOCATION = options.auth_file
        else:
            print "[!] Please verify path for .ovpn files directory AND authentication text file locations"
            exit(1)
    if options.check:
        check_process(True)
        exit(0)
    if not os.geteuid() == 0:
        print "[!] Script must run with 'sudo'. Help -> sudo python openvpn_auto.py -h"
        exit(1)
    if options.kill:
        kill()
    location = menu()
    start_opevpn(location)
