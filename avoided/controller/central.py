#!/usr/bin/env python
from __future__ import absolute_import
import SocketServer
import socket
import os
import LidarProcessor


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ArgContainer():
    def __init__(self, msg, server):
        self.msg = msg
        self.server = server

    def printMe(self):
        print self.msg


class CentralServer():
    # ADDR = "localhost"
    ADDR = "0.0.0.0"
    PORT = 3343
    SERVER = None
    DELIM = "\n"
    lidarDataQueue = None

    class TCPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            print "data rx"
            try:
                while True:
                    self.data = unicode(self.request.recv(1024),
                                        "utf-8").strip()
                    if len(self.data) == 0:
                        break
                    if self.server.root.lidarDataQueue is not None:
                        self.server.root.lidarDataQueue.put(self.data)
            except socket.timeout:
                print "connection timed out"
            except socket.error:    # connection closed
                print "connection closed"
                pass

    def killServer(self):
        self.SERVER.shutdown()
        self.SERVER.server_close()

    def startServer(self):
        try:
            os.unlink(self.ADDR)
        except OSError:
            if os.path.exists(self.ADDR):
                raise
        self.SERVER = ThreadedTCPServer((self.ADDR, self.PORT),
                                        self.TCPHandler)
        self.SERVER.root = self
        self.SERVER.serve_forever()


if __name__ == '__main__':
    udsServer = CentralServer()
    lp = LidarProcessor.LidarProcessor()
    udsServer.lidarDataQueue = lp.LIDAR_DATA_BUF  # register buffer
    print udsServer.lidarDataQueue
    lp.startListening()         # begin processing incoming data in new thread
    udsServer.startServer()     # begin listening for lidar data
