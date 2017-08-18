#!/usr/bin/env python
from __future__ import absolute_import
import SocketServer
import socket
import os
import observable
import cmdparser
import thread
import Queue
import WhipperSnapper


q = Queue.Queue()


class ArgContainer():
    def __init__(self, msg, server):
        self.msg = msg
        self.server = server

    def printMe(self):
        print self.msg


class CentralServer(observable.Observable):
    ADDR = "localhost"
    PORT = 3343
    SERVER = None
    DELIM = "\n"

    class TCPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            print "data rx"
            try:
                while True:
                    self.data = unicode(self.request.recv(1024),
                                        "utf-8").strip()
                    if len(self.data) == 0:
                        break
                    # a = ArgContainer(self.data, self.server.root)
                    q.put(self.data)
                    # self.server.root.notifyObservers(arg=a)
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
        self.SERVER = SocketServer.TCPServer((self.ADDR, self.PORT),
                                             self.TCPHandler)
        self.SERVER.root = self
        self.SERVER.serve_forever()


class LidarProcessor(observable.Observer):
    parser = cmdparser.CmdParser()
    sensorData = {}
    dataReceived = False  # will not start controlling until sensor data rx
    threshold = 400
    isMoving = False
    isRotating = False
    busy = False
    pointsBelow = 0      # count how many below threshold before stopping

    def __init__(self):
        for i in xrange(360):
            self.sensorData[i] = 0

    def update(self, arg):
        if arg is None:
            print u"I've been updated with no arg."
        else:
            # sections = str(arg.msg).split(",")
            datapairs = str(arg).split(";")
            datapairs = filter(None, datapairs)
            for datapair in datapairs:
                sections = datapair.split(",")
                if len(sections) is 2:
                    # print str(sections[0]) + "\t" + str(sections[1])
                    try:
                        deg = int(float(sections[0]))
                        dist = int(float(sections[1]))
                    except:
                        print sections[0] + " " + sections[1]
                        break
                    self.sensorData[deg] = dist  # [deg][dist]
                    if (self.isMoving and (deg < 30 or deg > 320) and
                            self.busy is False and self.isRotating is False):
                        if dist < self.threshold:
                            self.pointsBelow += 1
                            if self.pointsBelow > 3:
                                # STOP MOTORS!!
                                print "STOPPING " + str(deg) + " " + str(dist)
                                self.pointsBelow = 0
                                WhipperSnapper.turnOffMotors()
                                self.isMoving = False
                    elif self.isRotating is True:
                        if self.getClearSide() == "FRONT":
                            print "STOPPING ROTATION TO MOVE FORWARD"
                            # tell motor to stop
                            WhipperSnapper.turnOffMotors()
                            self.isRotating = False
                            # and go forward
                            WhipperSnapper.goForward()
                            self.isMoving = True
                        pass
                    elif self.isMoving is False and self.busy is False \
                            and self.isRotating is False: 
                        # look for open areas after a full 360 scan
                        side = self.getClearSide()
                        print "GOING TO " + side
                        if side is "RIGHT":
                            # rotateRight
                            WhipperSnapper.rotateRight()
                            self.isRotating = True
                        elif side is "LEFT":
                            # rotateleft
                            WhipperSnapper.rotateLeft()
                            self.isRotating = True
                            # blocking function
                            pass
                        elif side is "FRONT":
                            # go forward
                            WhipperSnapper.goForward()
                            self.isMoving = True
                            pass
                        elif side is "REAR":
                            WhipperSnapper.turnOffMotors()
                            # reverse?
                            pass
                        else:
                            pass
                else:
                    # print "WHAT: " + str(datapair) + " - " + str(datapairs)
                    # for sec in sections:
                    #     print "\t" + str(sec)
                    pass

    def getClearSide(self):
        rightAverage = 0
        leftAverage = 0
        frontAverage = 0

        ignoreFrontAverage = False  # ignore front opt if anything too close

        points = 0
        for i in xrange(0, 30):
            if self.sensorData[i] > self.threshold and self.sensorData[i] != 0:
                frontAverage += self.sensorData[i]
                points += 1
            elif self.sensorData[i] != 0:
                ignoreFrontAverage = True
                break
                # print "SKIPPING DATA " + str(i) \
                #     + " " + str(self.sensorData[i])
                # break

        for i in xrange(320, 359):
            if self.sensorData[i] > self.threshold and self.sensorData[i] != 0:
                frontAverage += self.sensorData[i]
                points += 1
            elif self.sensorData[i] != 0:
                # print "ignoring " + str(i) + "\t" + str(self.sensorData[i])
                ignoreFrontAverage = True
                break
            else:
                pass

        if points > 0:
            frontAverage = frontAverage / points

        points = 0
        for i in xrange(45, 135):
            if self.sensorData[i] != 0:
                rightAverage += self.sensorData[i]
                points += 1
        if points > 0:
            rightAverage = rightAverage / points

        points = 0
        for i in xrange(225, 315):
            if self.sensorData[i] != 0:
                leftAverage += self.sensorData[i]
                points += 1
        if points > 0:
            leftAverage = leftAverage / points

        # print str(leftAverage) + " " + str(frontAverage) \
        #     + " " + str(rightAverage)

        if ignoreFrontAverage is False and frontAverage > self.threshold:
            return "FRONT"
        elif rightAverage > self.threshold:
            if rightAverage >= leftAverage:
                return "RIGHT"
            elif leftAverage > self.threshold:
                return "LEFT"
            else:
                return "NONE"
        elif leftAverage > self.threshold:
            if leftAverage >= rightAverage:
                return "LEFT"
            elif rightAverage > self.threshold:
                return "RIGHT"
            else:
                return "NONE"
        else:
            return "NONE"


def processLidar(lidarProcessor):
    while True:
        e = q.get()
        lidarProcessor.update(e)


if __name__ == '__main__':
    udsServer = CentralServer()
    obs = LidarProcessor()
    # udsServer.addObserver(obs)
    thread.start_new_thread(processLidar, (obs,))
    udsServer.startServer()
