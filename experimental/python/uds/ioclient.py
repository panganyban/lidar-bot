#!/usr/bin/env python3
import socket
import select
import threading

class IOClient():
    ADDR = "/tmp/uds.sock"
    DELIM = "\n"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socketLock = threading.Lock()

    def connect(self):
        try:
            self.sock.connect(self.ADDR)
            return True
        except:
            return False


    """
    msg: pass in [TYPE] and [CODE]. Will format using protocol
    returns: message received if available otherwise returns empty str
    """
    def sendCommand(self, msg, timeout=1):
        try:
            if self.socketLock.acquire(timeout=1) is False:
                raise TimeoutError
            try:
                self.sock.sendall(bytes("{c>"+msg+"}", "utf-8"))
            except socket.error  as e:
                if(e.errno == socket.errno.EPIPE):
                    print("Server disconnected")
                else:
                    print("Socket error ", e)
            ready = select.select([self.sock], [], [], timeout)
            if ready[0]:
                response = str(self.sock.recv(1024), "utf-8")
                self.socketLock.release()
                return response
            else:
                self.socketLock.release()
                return ""
        except socket.timeout:
            print("socket not connected")
            return ""
        except TimeoutError:
            print("unable to acquire lock")
            return ""

