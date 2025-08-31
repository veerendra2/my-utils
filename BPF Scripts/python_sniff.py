'''
Description: Uses RAW SOCKET to sniff the traffic on specific interface.
NOTE: BPF Filters are not applied!
'''
import socket, struct
from binascii import hexlify
import nmap
import subprocess
import potsdb
import time

tsdbIp="52.8.104.253"
tsdbPort=4343
metrics1="port.details"
metrics2="connections.details"
interval=60

class Sniff:
    def __init__(self, interface_name):
        self.interface_name = interface_name
        # The raw in (listen) socket is a L2 raw socket that listens
        # for all packets going through a specific interface.
        self.ins = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 3)
        self.ins.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
        self.ins.bind((self.interface_name, 3))
        self.filters_list=list()
        self.nm=nmap.PortScanner()
        print "Looking for open port in localhost..."
        self.nmap_result=dict(self.nm.scan("127.0.0.1"))
        self.openPorts=dict()
        for ports, port_data in self.nmap_result["scan"]["127.0.0.1"]["tcp"].iteritems(): # Collects the open TCP ports
            self.openPorts.setdefault(ports,
                            [port_data["state"],
                            port_data["name"],
                            port_data["product"],
                            0,0])#in, out
        #print self.openPorts

    def __process_ipframe(self,pkt_type,raw_packet):
        ip_header_lenght=int(raw_packet[29],16)
        offset_port=((ip_header_lenght*32)/8)+14
        port_position=(offset_port*2)
        src_port=int(raw_packet[port_position:port_position+4],16)
        dst_port=int(raw_packet[port_position+4:port_position+8],16)
        if pkt_type == socket.PACKET_OUTGOING:
            if src_port in openPorts: #Out
                self.openPorts[src_port][3]=openPorts[src_port][3]+1
        else:
            if dst_port in openPorts: #In
                self.openPorts[dst_port][4]=openPorts[dst_port][4]+1

    def recv(self,timeout):
        while True:
            if timeout<=int(time.time()):
                pkt, sa_ll = self.ins.recvfrom(65535)
                print hexlify(pkt)
                self.__process_ipframe(sa_ll[2],hexlify(pkt))
            else:
                print "Sniffing Completed>",time.strftime("%I:%M:%S")
                break

class SendMetrics():
    def __init__(self,open_ports):
        self.metrics = potsdb.Client(tsdbIp, port=tsdbPort,qsize=1000, host_tag=True, mps=100, check_host=True)
        self.open_ports=open_ports

    def pushMetrics(self):
        for ports, details in self.open_ports.iteritems():
            self.metrics.send(metrics1,
                        details[3],
                        port=ports,
                        state=details[0],
                        pktout=details[4])
            print metrics1,str(details[3]),"port="+str(ports)+", state="+str(details[0])+", pktin="+str(details[4])
        for lines in subprocess.check_output("ss -tun4 | tail -n+2",shell=True).split("\n"):
            if lines and not "127.0.0.1" in lines:
                values=lines.split()
                self.metrics.send(metrics2,1,
                            scrip=values[4].split(":")[0],
                            dstip=values[5].split(":")[0],
                            dstport=values[5].split(":")[1])
                print metrics2,1,"scrip="+values[4].split(":")[0]+", dstip="+values[5].split(":")[0]+", dstport="+values[5].split(":")[1]
        self.metrics.wait()

if __name__=="__main__":
    ip_sniff=Sniff('wlan0')
    ip_sniff.recv(int(time.time())+interval)
    print ip_sniff.openPorts
    mts=SendMetrics(ip_sniff.openPorts)
    mts.pushMetrics()
