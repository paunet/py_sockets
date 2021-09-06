# import socket
# import struct

# MCAST_GRP = '224.0.1.129'
# MCAST_PORT = 320
# IS_ALL_GROUPS = True

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# if IS_ALL_GROUPS:
#     # on this port, receives ALL multicast groups
#     sock.bind(('', MCAST_PORT))
# else:
#     # on this port, listen ONLY to MCAST_GRP
#     sock.bind((MCAST_GRP, MCAST_PORT))
# mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


# print("Awaiting packets....")
# while True:
#     # For Python 3, change next line to "print(sock.recv(10240))"
#     print(sock.recv(10240))

#!/usr/bin/env python

import socket
import binascii

def main():
    MCAST_GRP = '172.16.255.255'#'224.0.1.129'
    MCAST_PORT = 320
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        pass
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock.bind((MCAST_GRP, MCAST_PORT))
    host = socket.gethostbyname(socket.gethostname()) 
    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
                    socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

    while 1:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.error as e:
            print('Expection')
            hexdata = binascii.hexlify(data)
            print('Data = %s' % hexdata)

if __name__ == '__main__':
  main()