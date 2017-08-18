#!/usr/bin/env python3
import select
import socket
import sys

HOST,PORT = "localhost", 9443
data = " ".join(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(data + "\n", "utf-8"), (HOST,PORT))
print("Sent:    {}".format(data))

ready = select.select([sock], [], [], 1)
if ready[0]:
    rx = str(sock.recv(1024), "utf-8")
    print("Rx  :    {}".format(rx))

