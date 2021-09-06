import socket
import struct
import ctypes

multicast_addr = '224.0.1.129'
bind_addr = '172.16.26.66' #☺0.0.0.0'
port = 319

def create_multicast_socket(bind_addr, multicast_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((bind_addr, port))
    return sock


PORTS = [319, 320]

sockets = []

for p in PORTS:
    sock = p, create_multicast_socket(bind_addr, multicast_addr, p)
    print(sock)
    sockets.append(sock)

while True:
    for port, socket in sockets:
        message, address = socket.recvfrom(255)
        print(f"DLC: {len(message)} Port: {port} Data: {message.hex()}")

    # message, address = sock2.recvfrom(255)
    # print(f"DLC: {len(message)} Port: {320} Data: {message}")
