#!/usr/bin/env python2
'''
Author : Veerendra Kakumanu
Description : Simple HTTP Server
'''
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
import argparse
import os

PROTOCOL = "HTTP/1.0"


def start_server(host, port, dir):
    server_address = (host, port)
    SimpleHTTPRequestHandler.protocol_version = PROTOCOL
    httpd = BaseHTTPServer.HTTPServer(server_address, SimpleHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    print "[*] Serving HTTP on {}:{}. Web Directory {}".format(sa[0], sa[1], dir)
    httpd.serve_forever()


if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = 8001
    WEB_DIRECTORY = os.getcwd()
    argument = argparse.ArgumentParser(description="Simple HTTP Server")
    argument.add_argument("-H", action="store", dest="host", help="Host IP. Default: 0.0.0.0")
    argument.add_argument("-p", action="store", dest="port", help="Port. Default: 8001")
    argument.add_argument("-d", action="store", dest="web_dir", help="Web Directory. Default: pwd")
    option = argument.parse_args()
    if option.host:
        HOST = option.host
    if option.port:
        try:
            PORT = int(option.port)
        except TypeError:
            print "[!] Port should be number."
            exit(1)
    if option.web_dir:
        if os.path.exists(option.web_dir):
            WEB_DIRECTORY = option.web_dir
            os.chdir(option.web_dir)
        else:
            print "[!] Invalid path, please check {}".format(option.web_dir)
            exit(1)
    start_server(HOST, PORT, WEB_DIRECTORY)
