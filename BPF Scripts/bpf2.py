from binascii import hexlify
from ctypes import create_string_buffer, addressof
from socket import socket, AF_PACKET, SOCK_RAW, SOL_SOCKET, PACKET_OUTGOING
from struct import pack, unpack


# A subset of Berkeley Packet Filter constants and macros, as defined in
# linux/filter.h.

# Instruction classes
BPF_LD = 0x00
BPF_JMP = 0x05
BPF_RET = 0x06

# ld/ldx fields
BPF_H = 0x08
BPF_B = 0x10
BPF_ABS = 0x20

# alu/jmp fields
BPF_JEQ = 0x10
BPF_K = 0x00

def bpf_jump(code, k, jt, jf):
    return pack('HBBI', code, jt, jf, k)

def bpf_stmt(code, k):
    return bpf_jump(code, k, 0, 0)


# Ordering of the filters is backwards of what would be intuitive for
# performance reasons: the check that is most likely to fail is first.
filters_list = [
    # Must have dst port 67. Load (BPF_LD) a half word value (BPF_H) in
    # ethernet frame at absolute byte offset 36 (BPF_ABS). If value is equal to
    # 67 then do not jump, else jump 5 statements.
    bpf_stmt(BPF_LD | BPF_H | BPF_ABS, 36),
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 8084, 1, 0),
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 9000, 0, 5),

    # Must be UDP (check protocol field at byte offset 23)
    bpf_stmt(BPF_LD | BPF_B | BPF_ABS, 23),
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 0x06, 0, 3),

    # Must be IPv4 (check ethertype field at byte offset 12)
    bpf_stmt(BPF_LD | BPF_H | BPF_ABS, 12),
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 0x0800, 0, 1),

    bpf_stmt(BPF_RET | BPF_K, 0x0fffffff), # pass
    bpf_stmt(BPF_RET | BPF_K, 0), # reject
]

# Create filters struct and fprog struct to be used by SO_ATTACH_FILTER, as
# defined in linux/filter.h.
filters = ''.join(filters_list)
b = create_string_buffer(filters)
mem_addr_of_filters = addressof(b)
fprog = pack('HL', len(filters_list), mem_addr_of_filters)

# As defined in asm/socket.h
SO_ATTACH_FILTER = 26

# Create listening socket with filters
s = socket(AF_PACKET, SOCK_RAW, 3)
s.setsockopt(SOL_SOCKET, SO_ATTACH_FILTER, fprog)
s.bind(('br-ex', 3))

def parseFrame(raw_packet,pkt_type):
    ip_header_lenght=int(raw_packet[29],16)
    #src_ip=socket.inet_ntoa(struct.pack('!I',"0x"+raw_packet[52:60]))
    #dst_ip=socket.inet_ntoa(struct.pack('!I',"0x"+raw_packet[60:68]))
    offset_port=((ip_header_lenght*32)/8)+14
    port_position=(offset_port*2)
    src_port=int(raw_packet[port_position:port_position+4],16)
    dst_port=int(raw_packet[port_position+4:port_position+8],16)
    if pkt_type == socket.PACKET_OUTGOING:
        print "SRC",src_port
        print "DST",dst_port
        print "+++++++++++++++++"
    else:
        print "SRC",src_port
        print "DST",dst_port
        print "=================="

while True:
    data, addr = s.recvfrom(65565)
    #print 'got data from', addr, ':', hexlify(data)
    parseFrame(hexlify(data),addr)
