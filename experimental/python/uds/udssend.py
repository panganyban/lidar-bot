#!/usr/bin/env python3
import socket
import sys
import select

addr = "/tmp/uds.sock"
# HOST,PORT = "localhost", 9443
data = " ".join(sys.argv[1:])
DELIM = "\n"

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.setblocking(0)
try:
    sock.connect(addr)
    print("connected to " + addr)
except:
    print("failed to connect to " + addr)
    sys.exit(1)

sock.sendall(bytes(data + "\r", "utf-8"))
rxMsg = ""
# sock.close()
ready = select.select([sock], [], [], 30)   # allow for 30 ms
if ready[0]:
    rxData = sock.recv(1024)
    rxMsg = str(rxData, "utf-8")
else:
    print("No response")

# eom = False
# while eom is False:
#     rxData = sock.recv(1024)
#     # print(str(rxData, "utf-8"))
#     if rxData: # data received
#         rxMsg += str(rxData, "utf-8")
#         if rxMsg.endswith(DELIM):
#             print("eom detected")
#             eom = True

print("Sent:    {}".format(data))
print("Recv:    {}".format(rxMsg))
sock.close()
sys.exit(1)


    

# ready = select.select([sock], [], [], 1)
# if ready[0]:
#     rx = str(sock.recv(1024), "utf-8")
#     print("Rx  :    {}".format(rx))

