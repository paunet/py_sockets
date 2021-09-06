# Multicast sender
# Guidance:  https://stackoverflow.com/a/1794373
import socket

MCAST_GRP = '224.0.1.129'
# MCAST_GRP = '224.1.1.1'
MCAST_PORT = 319
MESSAGE = b'Hello, Multicast from local!'

# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

MESSAGE_S  = b'\x00\x02\x00,\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d1P\xff\xfe\x82Z\xcd\x00\x01\x07\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
MESSAGE_F  = b'\x08\x02\x00,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d1P\xff\xfe\x82Z\xcd\x00\x01\x07\xb4\x02\x00\x00\x00\x12\xe1;\xbf\x03\xcdVD'
MESSAGE_S2 = b'\x00\x02\x00,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d1P\xff\xfe\x82Z\xcd\x00\x01\x07\xb4\x00\x00\x00\x00\x12\xe1;\xbf\x03\xcdVD'


l_msg = [MESSAGE_S, MESSAGE_S, MESSAGE_S2]

# for msg in l_msg:
    # print(len(msg))

sock.sendto(MESSAGE_S2, (MCAST_GRP, MCAST_PORT))
sock.close()