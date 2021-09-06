import socket
import struct
import ctypes

multicast_addr = '224.0.1.129'
bind_addr = '172.16.26.66' #☺0.0.0.0'
bind_addr = '0.0.0.0'
port = 319

def create_multicast_socket(bind_addr, multicast_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((bind_addr, port))
    return sock


# import ctypes
# from .desc_magnetics_MainFPGAStatus_v2 import MainFPGAStatus

class PTPHeader(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
	('message_type',            ctypes.c_uint8, 4),     # 0
    ('transport_specific',      ctypes.c_uint8, 4),
	('versionPTP',              ctypes.c_uint8, 4),     # 1
    ('-',                       ctypes.c_uint8, 4),
    ('message_length',          ctypes.c_uint16),       # 2 - 3
    ('domain_number',           ctypes.c_uint8),        # 4
    ('byte1',                   ctypes.c_uint8 * 30),   # 5
    ]

class PTPBasic(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
	('header',           PTPHeader),
	('epoch',            ctypes.c_uint16),
    ('seconds',          ctypes.c_uint32),
    ('nanos',            ctypes.c_uint32),
    
    ]


def struct_unpack(structure, raw_data):
    """
    Convert *raw_data* to an instance of *structure*.
 
    :param structure: The structure that describes *raw_data*.
    :type structure: :py:class:`ctypes.Structure`
    :param str raw_data: The binary string which contains the structures data.
    :return: A new instance of *structure*.
    :rtype: :py:class:`ctypes.Structure`
    """
    if not isinstance(structure, ctypes.Structure):
        structure = structure()
    ctypes.memmove(ctypes.byref(structure), raw_data, ctypes.sizeof(structure))
    return structure


def print_ptp_frame_info(frame):
    print(frame.header.message_length)
    print(frame.header.domain_number)
    print(frame.epoch)
    print(frame.seconds)
    print(frame.nanos)

def parse_PTP_packets(port, data):
    if len(data) == 44:
        if port == 319:
            print("sync  ", end=' ')
        else:
            print("follow", end=' ')
        # ptp_sync = PTPHeader()
        ptp_sync = struct_unpack(PTPBasic, data)
        print_ptp_frame_info(ptp_sync)

    # elif port == 320 and len(data) == 64:
    #     # ptp_sync = PTPHeader()
    #     ptp_sync = struct_unpack(PTPBasic, data)
    #     print(ptp_sync.header.message_length)
    #     print(ptp_sync.header.domain_number)


PORTS = [319, 320]

sockets = []

for p in PORTS:
    sock = p, create_multicast_socket(bind_addr, multicast_addr, p)
    sockets.append(sock)

while True:
    for port, socket in sockets:
        message, address = socket.recvfrom(255)
        # print(f"DLC: {len(message)} Port: {port} Data: {message.hex()}")
        print(f"DLC: {len(message)} Port: {port} Data: {message}")
        # parse_PTP_packets(port, message)

    # message, address = sock2.recvfrom(255)
    # print(f"DLC: {len(message)} Port: {320} Data: {message}")
