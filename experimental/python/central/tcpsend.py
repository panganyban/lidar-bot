#!/usr/bin/env python
from __future__ import absolute_import
import socket
import sys
import select

addr = "localhost"
port = 3343
# HOST,PORT = "localhost", 9443
data = u" ".join(sys.argv[1:])
DELIM = u"\n"

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setblocking(0)
try:
    sock.connect((addr, port))
    print u"connected to " + addr
except:
    print u"failed to connect to " + addr
    sys.exit(1)

print "sending" + data
sock.sendall(str(data + "\n").encode("utf-8"))
rxMsg = u""
# sock.close()
ready = select.select([sock], [], [], 30)   # allow for 30 ms
if ready[0]:
    rxData = sock.recv(1024)
    rxMsg = unicode(rxData, u"utf-8")
else:
    print u"No response"

# eom = False
# while eom is False:
#     rxData = sock.recv(1024)
#     # print(str(rxData, "utf-8"))
#     if rxData: # data received
#         rxMsg += str(rxData, "utf-8")
#         if rxMsg.endswith(DELIM):
#             print("eom detected")
#             eom = True

print u"Sent:    {}".format(data)
print u"Recv:    {}".format(rxMsg)
sock.close()
sys.exit(1)

# ready = select.select([sock], [], [], 1)
# if ready[0]:
#     rx = str(sock.recv(1024), "utf-8")
#     print("Rx  :    {}".format(rx))
