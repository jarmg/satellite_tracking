# Not sure which approach to use:

'''
Problem is that, I can find the camera on the network
through a upnp broadcast discovery but the xml seems to
indicate that the device offers no services?

Maybe they are using upnp for device discovery only and using
something else for acctual commands?


'''


#1:
import upnpclient as upnp

devices = upnpclient.discover()


#2 socket:
import socket

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(2)
s.sendto(bytes(msg, encoding='ascii'), ('239.255.255.250', 1900) )

try:
    while True:
        data, addr = s.recvfrom(65507)
        print(addr, data)
        print("\n\n")
except socket.timeout:
    pass