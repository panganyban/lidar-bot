#!/usr/bin/env python
from __future__ import absolute_import
import socket
import select
import threading
import sys


class IOClient(object):
    ADDR = u"localhost"
    PORT = 3343
    DELIM = u"\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketLock = threading.Lock()

    def connect(self):
        try:
            self.sock.connect((self.ADDR, self.PORT))
            return True
        except:
            print sys.exc_info()[0]
            return False

    def close(self):
        print "closing"
        self.sock.close()

    def sendRawData(self, msg, timeout=1):
        try:
            if self.socketLock.acquire(1) is False:
                return
                # raise TimeoutError
            try:
                self.sock.sendall(str(msg).encode("utf-8"))
            except socket.error, e:
                if(e.errno == socket.errno.EPIPE):
                    print u"Server disconnected"
                else:
                    print u"Socket error ", e

            ready = select.select([self.sock], [], [], timeout)
            if ready[0]:
                response = unicode(self.sock.recv(1024), u"utf-8")
                self.socketLock.release()
                return response
            else:
                self.socketLock.release()
                return u""
        except socket.timeout:
            print u"socket not connected"
            return False
        except Exception as e:
            print "Exception: " + str(e)
            return False

    u"""
    msg: pass in [TYPE] and [CODE]. Will format using protocol
    returns: message received if available otherwise returns empty str
    """
    def sendCommand(self, msg, timeout=1):
        try:
            if self.socketLock.acquire(1) is False:
                return
                # raise TimeoutError
            try:
                self.sock.sendall(str("{c>" + msg + "}").encode("utf-8"))
            except socket.error, e:
                if(e.errno == socket.errno.EPIPE):
                    print u"Server disconnected"
                else:
                    print u"Socket error ", e

            ready = select.select([self.sock], [], [], timeout)
            if ready[0]:
                response = unicode(self.sock.recv(1024), u"utf-8")
                self.socketLock.release()
                return response
            else:
                self.socketLock.release()
                return u""
        except socket.timeout:
            print u"socket not connected"
            return False
        except Exception as e:
            print "Exception: " + e
            return False
        # except TimeoutError:
        #     print u"unable to acquire lock"
        #     return u""
