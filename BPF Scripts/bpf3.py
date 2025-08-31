'''
Author: OpsMx
Description:
1) Gets the cummulative packet and byte count on open TCP ports
2) Gets the actives connections/ connected peers
Refer: http://allanrbo.blogspot.in/2011/12/raw-sockets-with-bpf-in-python.html
Required Packages: nmap
'''
from binascii import hexlify
from ctypes import create_string_buffer, addressof
from socket import socket, AF_PACKET, SOCK_RAW, SOL_SOCKET, PACKET_OUTGOING
from struct import pack, unpack
import subprocess
import potsdb
import time
import threading
import re

tsdbIp="52.8.104.253"
tsdbPort=4343
metrics1="port.details"
metrics2="connections.details"
interval=10

class OpensPorts(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ports=dict()
        self.lock=threading.RLock()

    def getPorts(self):
        with self.lock:
            copy_ports=self.ports
        return copy_ports

    def run(self):
        while True:
            tmp=dict()
            for line in subprocess.check_output("nmap localhost | tail -n+7", shell=True).split('\n'):
                if line and not re.search(r'Nmap done',line) and not re.search(r'PORT',line):
                    tmp.setdefault(int(line.split("/")[0]), line.split()[2])
            with self.lock:
                self.ports=tmp

class BPFSniff():
#A subset of Berkeley Packet Filter constants and macros, as defined in linux/filter.h.
    def __init__(self,interface='wlan0'): #Args--> Interface,
        self.interface=interface
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
        self.new_open_ports=dict()
        self.lock=threading.RLock()

    def getSocket(self,openPorts_Object):#Args "OpensPorts" Class Object
        tmp=dict()
        filters_list=list()
        while True:
            if openPorts_Object.getPorts(): #Got atleast one port
                break
            else:
                #Keep trying for ports
                time.sleep(5)

        thread_ports=openPorts_Object.getPorts()
        for port, name in thread_ports.items():
            if port in self.new_open_ports:
                tmp[port]=self.new_open_ports[port]
            else:
                tmp[port]=[name,0,0,0,0] #BytesIn, BytesOut, PacketsIn, PacketsOut

        self.new_open_ports=tmp
        print "PORTS>",self.new_open_ports
        print "+++++++++++++++++++"
        instruction_count_dst=len(self.new_open_ports)-1
        instruction_count_src=len(self.new_open_ports)*2
        #dummy=list()
        #Source Port Filters
        filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_H | self.BPF_ABS, 34))
        for ports in self.new_open_ports:
            self.filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, ports, instruction_count_src, 0))
            #dummy.append([port,instruction_count_src,0])
            instruction_count_src=instruction_count_src-1

        #Destination Port Filters
        filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_H | self.BPF_ABS, 36))
        for ports in self.new_open_ports:
            if instruction_count_dst!=0:
                filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, ports, instruction_count_dst, 0))
                #dummy.append([port,instruction_count_dst,0])
            else:
                filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, ports, 0, 5))
                #dummy.append([port,0,5])
            instruction_count_dst=instruction_count_dst-1


        # Must be TCP (check protocol field at byte offset 23)
        filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_B | self.BPF_ABS, 23))
        filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, 0x06, 0, 3))

        # Must be IPv4 (check ethertype field at byte offset 12)
        filters_list.append(self.bpf_stmt(self.BPF_LD | self.BPF_H | self.BPF_ABS, 12))
        filters_list.append(self.bpf_jump(self.BPF_JMP | self.BPF_JEQ | self.BPF_K, 0x0800, 0, 1))

        filters_list.append(self.bpf_stmt(self.BPF_RET | self.BPF_K, 0x0fffffff)) #pass
        filters_list.append(self.bpf_stmt(self.BPF_RET | self.BPF_K, 0))  #reject

        filters = ''.join(filters_list)
        b=create_string_buffer(filters)
        mem_addr_of_filters = addressof(b)
        fprog=pack('HL', len(filters_list), mem_addr_of_filters)
        # As defined in asm/socket.h
        SO_ATTACH_FILTER = 26
        # Create listening socket with filters
        s=socket(AF_PACKET, SOCK_RAW, 3)
        s.setsockopt(SOL_SOCKET, SO_ATTACH_FILTER, fprog)
        s.bind((self.interface, 3)) # "3" is for bidirectional traffic
        return s #Returning Socket

    def bpf_jump(self,code, k, jt, jf):
        return pack('HBBI', code, jt, jf, k)

    def bpf_stmt(self,code, k):
        return self.bpf_jump(code, k, 0, 0)

    def __parseFrame(self,raw_packet,pkt_type,len):
        ip_header_lenght=int(raw_packet[29],16)
        #src_ip=socket.inet_ntoa(struct.pack('!I',"0x"+raw_packet[52:60]))
        #dst_ip=socket.inet_ntoa(struct.pack('!I',"0x"+raw_packet[60:68]))
        offset_port=((ip_header_lenght*32)/8)+14
        port_position=(offset_port*2)
        src_port=int(raw_packet[port_position:port_position+4],16)
        dst_port=int(raw_packet[port_position+4:port_position+8],16)
        #print "SRC",src_port,"DST",dst_port
        if pkt_type==PACKET_OUTGOING:
            if src_port in self.new_open_ports: #Out
                self.new_open_ports[src_port][4]=self.new_open_ports[src_port][4]+1
                self.new_open_ports[src_port][2]=self.new_open_ports[src_port][2]+len #Bytes
        else:
            if dst_port in self.new_open_ports: #In
                self.new_open_ports[dst_port][3]=self.new_open_ports[dst_port][3]+1
                self.new_open_ports[dst_port][1]=self.new_open_ports[dst_port][1]+len #Bytes

    def sniff(self,sock):
        print self.new_open_ports
        epoch_end=int(time.time())+interval
        while True:
            data, addr = sock.recvfrom(65535)
            #print 'got data from', addr, ':', hexlify(data)
            port=self.__parseFrame(hexlify(data),addr,len(data))
            if epoch_end<=int(time.time()):
                print "\nCompleted..."
                break


class ActiveConnections():
    def __init__(self):
        self.tcp_file="/proc/net/tcp"
        self.tcp_states={"01":"TCP_ESTABLISHED",
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
                        "0C":"TCP_MAX_STATES"}
        self.connections=list()

    def getConnections(self):
        with open(self.tcp_file,'r') as file:
            for line in file.readlines():
                parts=line.split()
                if(parts[3]=="01" and not re.search(r'sl',line)
                                and not re.search(r'00000000',parts[1])
                                and not re.search(r'0100007F',parts[1])):
                    #local_ip=socket.inet_ntoa(struct.pack('<L',int(parts[1].split(":")[0],16)))
                    local_port=int(parts[1].split(":")[1],16)
                    peer_ip=socket.inet_ntoa(struct.pack('<L',int(parts[2].split(":")[0],16)))
                    peer_port=int(parts[2].split(":")[1],16)
                    self.connections.append(peer_ip,peer_port,local_port)
                    print metrics2,1,"peerip",peer_ip,"peerport",peer_port,"localport",local_port
        return self.connections


class SendMetrics():
    def __init__(self,open_ports, connections):
        self.metrics = potsdb.Client(tsdbIp, port=tsdbPort,qsize=1000, host_tag=True, mps=100, check_host=True)

    def push(self):
        pass
        metrics.wait()


pts=OpensPorts()
pts.daemon=True
pts.start()
bpf=BPFSniff("br-ex")

if __name__=='__main__':
    while True:
        bpf.sniff(bpf.getSocket(pts))
        print bpf.new_open_ports
