#!/usr/bin/env python3
import socketserver
import socket
from queue import Queue
import threading


class IOCmder():
    HOST = "localhost"
    PORT = 9443
    ID = "SERVER"
    OBS = 0
    
    class UDPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            # data = self.request[0].strip()
            data = self.request[0]
            socket = self.request[1]
            data_str = data.decode("utf-8")
            # print(data_str)
            print(self.server.testObj.ID)
            self.server.testObj.notifyObservers(data_str)
            socket.sendto(data.upper(), self.client_address)

    def startListener(self):
        socketserver.UDPServer.allow_reuse_address = True
        server = socketserver.UDPServer((self.HOST,self.PORT), self.UDPHandler)
        server.testObj = self
        server.serve_forever()

    def registerObserver(self, obs):
        self.OBS = obs
        pass

    def deleteObserver(self, obs):
        pass

    def notifyObservers(self, msg):
        print("Notifying observers!" + msg)
        self.OBS.update(msg)
        pass

class Listener():
    def update(self, msg):
        print("got the msg: " + msg)
    
if __name__ == '__main__':
    pool = Queue()
    cmder = IOCmder()
    obs = Listener()
    cmder.registerObserver(obs)
    print("Starting server")
    t = threading.Thread(target=cmder.startListener)
    t.setDaemon(True)
    t.start()
    pool.put(t)
    # threads.append(t)
    # cmder.startListener()
    print("Server running")
    pool.join()
