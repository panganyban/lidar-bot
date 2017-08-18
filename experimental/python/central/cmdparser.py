#!/usr/bin/env python

# Still WIP. Just trying to find a nice way to identify commands...

from __future__ import absolute_import


class Cmds():
    GetAllMotorStatuses = 0
    GetSingleMotorStatus = 1
    SetMotorSpeed = 2
    TurnCar = 3
    Invalid = 4


class CmdParser(object):

    def parseCommand(self, command):
        if(self.validateCommand(command) is True):
            meat = (self.getMeat(command))
            return self.defineMeat(meat)
        else:
            return Cmds.Invalid

    def validateCommand(self, command):
        if(command.startswith(u'{c>') and command.endswith(u'}')):
            return True
        else:
            return False

    def getMeat(self, command):
        meat = u""
        meat = command.strip(u"{c>")
        meat = meat.strip(u"}")
        return meat

    def defineMeat(self, meat):
        if(meat.startswith(u"M")):
            # motor related command
            if(meat == u"M?"):
                return Cmds.GetAllMotorStatuses
            elif(len(meat) == 3 and meat.endswith(u"?")):
                return Cmds.GetSingleMotorStatus
            elif(len(meat) >= 4 and meat.find(u";") == 2):
                # specific motor status?
                splitMeat = meat.split(u';')
                print u"\tSet motor " + splitMeat[0][1] \
                    + u" to speed " + splitMeat[1]

                return Cmds.SetMotorSpeed
            else:
                return Cmds.Invalid


# testing
# parser = CmdParser()
#
# print(parser.parseCommand("c>M?"))
# print(parser.parseCommand("{c>M?}"))
# print(parser.parseCommand("{c>M1?}"))
# print(parser.parseCommand("{c>M1;233}"))
# print(parser.parseCommand("{c>M12;233}"))
