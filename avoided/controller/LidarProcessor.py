#!/usr/bin/env python
from __future__ import absolute_import
import threading
import Queue
import atexit

ENABLE_WHIPPERSNAPPER = True

if ENABLE_WHIPPERSNAPPER:
    import WhipperSnapper
    WhipperSnapper.TURN_SPEED = 230
    WhipperSnapper.LEFT_SPEED = 160
    WhipperSnapper.RIGHT_SPEED = 160


class LidarProcessor():
    LIDAR_DATA_BUF = Queue.Queue()  # incoming data streamed here
    MIN_THRESHOLD = 450      # minimum distance in front
    MAX_MISSES = 20          # maximum numb of points too close
    FRONT_RANGE = [30, 320]  # front in between [1] and [0] (CIRCLE)
    RIGHT_RANGE = [45, 135]  # right in between [0] and [1] (unlike FRONT)
    LEFT_RANGE = [225, 315]  # left  in between [0] and [1] (unlike FRONT)
    sensorData = {}          # dictionary of sensor data {deg, distance}
    isMovingFwd = False      # flag to signal if car is moving fwd or not
    isRotating = False       # flag to signal if car is rotating or not
    pointsTooClose = 0       # count how many below threshold before stopping
    _listenThread = None     # thread used to process incoming lidar data
    ignoreLidar = False      # overridable lidar processing flag

    def __init__(self):
        for i in xrange(360):
            self.sensorData[i] = 0

    def stopListening(self):
        """Shuts down listener"""
        if self._listenThread is not None:
            self._listenThread.stop()
            self._listenThread.join()

    def startListening(self):
        """Creates a thread to begin checking its data buffer
        for data to process"""
        self._listenThread = threading.Thread(target=self._processLidar)
        self._listenThread.daemon = True
        self._listenThread.start()

    def update(self, arg):
        """Updates processor with new incoming data from RPLidar and calculates
        if any object is in the way or not to make a decision on movement.

        Parameters
        ----------
        arg : str
            RPLidar data stream with format: deg,dist;deg,dist;deg,dist...
        """
        if arg is None:
            print u"I've been updated with no arg."
        elif self.ignoreLidar is False:
            # split up incoming data stream if needed
            # deg,dist;deg,dist;deg,dist;
            datapairs = str(arg).split(";")
            datapairs = filter(None, datapairs)

            # begin processing newly received data
            for datapair in datapairs:
                sections = datapair.split(",")  # split {deg, dist}
                if len(sections) is 2:
                    try:
                        deg = int(float(sections[0]))
                        dist = int(float(sections[1]))
                    except:
                        print sections[0] + " " + sections[1]
                        break
                    # import sensor data into dictionary
                    self.sensorData[deg] = dist  # [deg][dist]

                    # begin algorithm for dodging obstacles
                    if (self.isMovingFwd and (self._angleIsFrontside(deg)) and
                            self.isRotating is False):
                        if dist < self.MIN_THRESHOLD:
                            self.pointsTooClose += 1
                            if self.pointsTooClose > self.MAX_MISSES:
                                # STOP MOTORS!!
                                print "STOPPING " + str(deg) + " " + str(dist)
                                self.pointsTooClose = 0
                                self._turnOffMotors()
                            elif deg > 357:
                                self.pointsTooClose = 0
                    elif self.isRotating is True:
                        if self.getClearSide() == "FRONT":
                            print "STOPPING ROTATION TO MOVE FORWARD"
                            # tell motor to stop
                            self._turnOffMotors()
                            # and go forward
                            self._goForward()
                        pass
                    elif self.isMovingFwd is False \
                            and self.isRotating is False:
                        # look for open areas after a full 360 scan
                        side = self.getClearSide()
                        print "GOING TO " + side
                        if side is "RIGHT":
                            # rotateRight
                            self._rotateRight()
                        elif side is "LEFT":
                            # rotateleft
                            self._rotateLeft()
                            # blocking function
                            pass
                        elif side is "FRONT":
                            # go forward
                            self._goForward()
                            pass
                        elif side is "REAR":
                            self._turnOffMotors()
                            # reverse?
                            pass
                        else:
                            pass
                else:
                    # print "WHAT: " + str(datapair) + " - " + str(datapairs)
                    # for sec in sections:
                    #     print "\t" + str(sec)
                    pass
        else:
            pass    # lidar processing was overridden. ignoring now.

    def getClearSide(self):
        """ Finds the clearest side (FRONT/LEFT/RIGHT) """
        rightAverage = 0
        leftAverage = 0
        frontAverage = 0
        ignoreFrontAverage = False  # ignore front opt if anything too close
        badFrontData = 0            # if too large, will not choose front
        points = 0

        # BEGIN CALCULATING FRONT ZONE
        for i in xrange(0, self.FRONT_RANGE[0]):
            if self.sensorData[i] != 0:
                if self.sensorData[i] >= self.MIN_THRESHOLD:
                    frontAverage += self.sensorData[i]
                    points += 1
                else:
                    badFrontData += 1
                    if badFrontData > self.MAX_MISSES:
                        ignoreFrontAverage = True

        for i in xrange(self.FRONT_RANGE[1], 359):
            if self.sensorData[i] != 0:
                if self.sensorData[i] >= self.MIN_THRESHOLD:
                    frontAverage += self.sensorData[i]
                    points += 1
                else:
                    badFrontData += 1
                    if badFrontData > self.MAX_MISSES:
                        ignoreFrontAverage = True

        if points > 0:
            frontAverage = frontAverage / points
        # DONE CALCULATING FRONT ZONE

        # BEGIN CALCULATING RIGHT ZONE
        points = 0
        for i in xrange(self.RIGHT_RANGE[0], self.RIGHT_RANGE[1]):
            if self.sensorData[i] != 0:
                rightAverage += self.sensorData[i]
                points += 1
        if points > 0:
            rightAverage = rightAverage / points
        # DONE CALCULATING RIGHT ZONE

        # BEGIN CALCULATING LEFT ZONE
        points = 0
        for i in xrange(self.LEFT_RANGE[0], self.LEFT_RANGE[1]):
            if self.sensorData[i] != 0:
                leftAverage += self.sensorData[i]
                points += 1
        if points > 0:
            leftAverage = leftAverage / points
        # DONE CALCULATING LEFT ZONE

        # NOW CHOOSE A SIDE. Prioritizes the front size.
        if ignoreFrontAverage is False and frontAverage > self.MIN_THRESHOLD:
            return "FRONT"
        elif rightAverage > self.MIN_THRESHOLD:
            if rightAverage >= leftAverage:
                return "RIGHT"
            elif leftAverage > self.MIN_THRESHOLD:
                return "LEFT"
            else:
                return "NONE"
        elif leftAverage > self.MIN_THRESHOLD:
            if leftAverage >= rightAverage:
                return "LEFT"
            elif rightAverage > self.MIN_THRESHOLD:
                return "RIGHT"
            else:
                return "NONE"
        else:
            return "NONE"

    def _angleIsFrontside(self, deg):
        """Checks if the deg passed in is in the front of the car

        Parameters
        ----------
        deg: int
            Degree value to test if it's in the front or not

        Returns
        -------
        True: if degree is in front
        Fale: if degree isn't in front
        """
        if deg < self.FRONT_RANGE[0] or deg >= self.FRONT_RANGE[1]:
            return True
        else:
            return False

    def processMoveCommand(self, arg):
        if arg == "GNULL":
            print "RESUME DATA PROCESSING"
            self.ignoreLidar = False
            return
        else:
            print "PAUSE DATA PROCESSING"
            self.ignoreLidar = True

        if arg == "GF":
            self._goForward()
        elif arg == "GB":
            self._goBackward()
        elif arg == "GS":
            self._turnOffMotors()
        elif arg == "GL":
            self._rotateLeft()
        elif arg == "GR":
            self._rotateRight()
            pass

    def _turnOffMotors(self):
        if ENABLE_WHIPPERSNAPPER:
            WhipperSnapper.turnOffMotors()
        self.isRotating = False
        self.isMovingFwd = False

    def _rotateLeft(self):
        if ENABLE_WHIPPERSNAPPER:
            if self.isRotating or self.isMovingFwd:
                self._turnOffMotors()
            WhipperSnapper.rotateLeft()
        self.isRotating = True

    def _rotateRight(self):
        if ENABLE_WHIPPERSNAPPER:
            if self.isRotating or self.isMovingFwd:
                self._turnOffMotors()
            WhipperSnapper.rotateRight()
        self.isRotating = True

    def _goForward(self):
        if ENABLE_WHIPPERSNAPPER:
            if self.isRotating or self.isMovingFwd:
                self._turnOffMotors()
            WhipperSnapper.goForward()
        self.isMovingFwd = True

    def _goBackward(self):
        if ENABLE_WHIPPERSNAPPER:
            if self.isRotating or self.isMovingFwd:
                self._turnOffMotors()
            WhipperSnapper.goBackward()
        self.isMovingFwd = True

    def _processLidar(self):
        while True:
            e = self.LIDAR_DATA_BUF.get()
            if e.startswith("G"):
                self.processMoveCommand(e)
            else:  # assume a deg-dist value
                self.update(e)

    atexit.register(stopListening)
