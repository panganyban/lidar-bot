#!/usr/bin/env python3


class MotorController():
    _motorCount = 4
    _motorStatuses = []

    def __init__(self):
        for x in range(0,self._motorCount):
            self._motorStatuses.append(0)

    def getMotorStatus(self, motorNumber):
        if(motorNumber == 0): # get all
            state = ""
            for i in range(0, self._motorCount):
                state += str(self._motorStatuses[i])
            return state
        elif(motorNumber <= self._motorCount):
            return str(self._motorStatuses[motorNumber - 1])
        else:
            return str(0)

