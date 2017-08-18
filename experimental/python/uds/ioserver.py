#!/usr/bin/env python3
import socket
import socketserver
from queue import Queue
import threading
import os
import observable
import motorcontroller
import cmdparser


class IOServer(observable.Observable):
    ADDR = "/tmp/uds.sock"
    SERVER = None
    DELIM = "\n"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    class UnixDomainSocketRequestHandler(socketserver.BaseRequestHandler):
        def handle(self):
            print("data rx")
            try:
                while True:
                    self.data = str(self.request.recv(1024), "utf-8").strip()
                    print(self.data)
                    self.request.sendall(bytes(self.data.upper() + "\n", "utf-8"))
                    self.server.root.notifyObservers(self.data)
                    if len(self.data) == 0:
                        print("no more data")
                        break
            except socket.timeout:
                print("connection timed out")
            except socket.error:    # connection closed
                pass

    def startServer(self):
        try:
            os.unlink(self.ADDR)
        except OSError:
            if os.path.exists(self.ADDR):
                raise
        self.SERVER = socketserver.UnixStreamServer(self.ADDR, \
                self.UnixDomainSocketRequestHandler)
        self.SERVER.root = self
        self.SERVER.serve_forever()


class Listener(observable.Observer):
    parser = cmdparser.CmdParser()
    mc = motorcontroller.MotorController()
    def update(self, arg):
        print("Updating...")
        if arg is None:
            print("I've been updated with no arg.")
        else:
            print(self.parser.parseCommand(arg))    # print received command

if __name__ == '__main__':
    udsServer = IOServer()
    obs = Listener()
    udsServer.addObserver(obs)

    print("Starting server")
    t = threading.Thread(target=udsServer.startServer)
    t.setDaemon(True)
    t.start()

    pool = Queue()
    pool.put(t)
    print("Server running")
    pool.join()
