#!/usr/bin/env python


class MotorController(object):
    _motorCount = 4
    _motorStatuses = []

    def __init__(self):
        for x in xrange(0, self._motorCount):
            self._motorStatuses.append(0)

    def getMotorStatus(self, motorNumber):
        if(motorNumber == 0):  # get all
            state = u""
            for i in xrange(0, self._motorCount):
                state += unicode(self._motorStatuses[i])
            return state
        elif(motorNumber <= self._motorCount):
            return unicode(self._motorStatuses[motorNumber - 1])
        else:
            return unicode(0)
