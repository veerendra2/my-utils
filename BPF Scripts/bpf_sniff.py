from binascii import hexlify
from ctypes import create_string_buffer, addressof
from socket import socket, AF_PACKET, SOCK_RAW, SOL_SOCKET
from struct import pack, unpack
import nmap
import subprocess
import potsdb
import os
import time
import sys


tsdbIp="52.8.104.253"
tsdbPort=4343
hostname = os.uname()[1]
metrics1="port.details"
metrics2="connections.details"
metrics = potsdb.Client(tsdbIp, port=tsdbPort,qsize=1000, host_tag=True, mps=100, check_host=True)
# A subset of Berkeley Packet Filter constants and macros, as defined in
# linux/filter.h.
interval=10
class BPFSniff():
    def __init__(self,interface='br-ex'):
        self.interface=interface
        self.spin=spinner()
        # Instruction classes
        self.BPF_LD = 0x00
        self.BPF_JMP = 0x05
        self.BPF_RET = 0x06
        # ld/ldx fields
        self.BPF_H = 0x08
        self.BPF_B = 0x10
        self.BPF_ABS = 0x20
        # alu/jmp fields
        self.BPF_JEQ = 0x10
        self.BPF_K = 0x00
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
                            0,0])
        print self.openPorts
        # Ordering of the filters is backwards of what would be intuitive for
        # performance reasons: the check that is most likely to fail is first.

        # Must have dst port 67. Load (BPF_LD) a half word value (BPF_H) in
        # ethernet frame at absolute byte offset 36 (BPF_ABS). If value is equal to
        # 67 then do not jump, else jump 5 statements.--> Appending to filters_list List
        self.filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_H | self.BPF_ABS, 36))
        for port in self.openPorts:
            print "PORT>",port
            self.filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, port, 0, 5))

        # Must be TCP (check protocol field at byte offset 23)
        self.filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_B | self.BPF_ABS, 23))
        self.filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, 0x06, 0, 3))

        # Must be IPv4 (check ethertype field at byte offset 12)
        self.filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_H | self.BPF_ABS, 12))
        self.filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, 0x0800, 0, 1))

        self.filters_list.append(self.bpf_stmt(self.BPF_RET | self.BPF_K, 0x0fffffff)) #pass
        self.filters_list.append(self.bpf_stmt(self.BPF_RET | self.BPF_K, 0))  #reject

    def bpf_jump(self,code, k, jt, jf):
        return pack('HBBI', code, jt, jf, k)

    def bpf_stmt(self,code, k):
        return self.bpf_jump(code, k, 0, 0)

    def parseFrame(self,raw_packet):
        ip_header_lenght=int(raw_packet[29],16)
        #src_ip=socket.inet_ntoa(struct.pack('!I',"0x"+raw_packet[52:60]))
        #dst_ip=socket.inet_ntoa(struct.pack('!I',"0x"+raw_packet[60:68]))
        offset_port=((ip_header_lenght*32)/8)+14
        port_position=(offset_port*2)
        src_port=int(raw_packet[port_position:port_position+4],16)
        dst_port=int(raw_packet[port_position+4:port_position+8],16)
        #print "SRC",src_port,"DST",dst_port
        return [src_port,dst_port]

    def getPackets(self):
        # Create filters struct and fprog struct to be used by SO_ATTACH_FILTER, as
        # defined in linux/filter.h.
        filters = ''.join(self.filters_list)
        b = create_string_buffer(filters)
        mem_addr_of_filters = addressof(b)
        fprog = pack('HL', len(self.filters_list), mem_addr_of_filters)

        # As defined in asm/socket.h
        SO_ATTACH_FILTER = 26

        # Create listening socket with filters
        s = socket(AF_PACKET, SOCK_RAW, 0x0800)
        s.setsockopt(SOL_SOCKET, SO_ATTACH_FILTER, fprog)
        s.bind((self.interface, 0x0800))
        epoch_end=int(time.time())+interval
        print "Counting Packets...",
        while True:
            #sys.stdout.write("\b{}".format(next(self.spin)))
            #sys.stdout.flush()
            data, addr = s.recvfrom(65535)
            #print 'got data from', addr, ':', hexlify(data)
            port=self.parseFrame(hexlify(data))
            try:
                self.openPorts[port[0]][4]=self.openPorts[port[0]][4]+1 #Out Packets
            except KeyError:
                try:
                    self.openPorts[port[1]][3]=self.openPorts[port[1]][3]+1 #Inpackets
                except:
                    pass
                pass
            if epoch_end<=int(time.time()):
                print "\nCompleted..."
                break
        return self.openPorts

def spinner():
    while True:
        for cursor in "/-\\|":
            yield cursor

class SendMetrics():
    def __init__(self,open_ports):
        self.metrics = potsdb.Client(tsdbIp, port=tsdbPort,qsize=1000, host_tag=True, mps=100, check_host=True)
        self.open_ports=open_ports

    def pushOpenPorts(self):
        for ports, details in self.open_ports.iteritems():
            self.metrics.send(metrics1,
                        details[3],
                        port=ports,
                        state=details[0],
                        pktout=details[4])
            print metrics1,str(details[3])+"port="+str(ports)+", state="+str(details[0])+", pktin="+str(details[4])
        for lines in subprocess.check_output("ss -tun4 | tail -n+2",shell=True).split("\n"):
            if lines:
                values=lines.split()
                metrics.send(metrics2,1,
                            scrip=values[4].split(":")[0],
                            dstip=values[5].split(":")[0],
                            dstport=values[5].split(":")[1])

                print metrics2,1,"scrip="+values[4].split(":")[0]+", dstip="+values[5].split(":")[0]+", dstport="+values[5].split(":")[1]
        metrics.wait()


if __name__=='__main__':
    #ports_dict={91:0,}
    while True:
        bpf=BPFSniff()
        pts=bpf.getPackets()
        mts=SendMetrics(pts)
        mts.pushOpenPorts()
        #mts.pushActiveConnections()
