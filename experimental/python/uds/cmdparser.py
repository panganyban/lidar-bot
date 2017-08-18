#!/usr/bin/env python3

# Still WIP. Just trying to find a nice way to identify commands...

from enum import Enum

class Cmds(Enum):
    GetAllMotorStatuses = 0
    GetSingleMotorStatus = 1
    SetMotorSpeed = 2
    TurnCar = 3
    Invalid = 4

class CmdParser():

    def parseCommand(self, command):
        if(self.validateCommand(command) == True):
            meat = (self.getMeat(command))
            return self.defineMeat(meat)
        else:
            return Cmds.Invalid

    def validateCommand(self, command):
        if(command.startswith('{c>') and command.endswith('}')):
            return True
        else:
            return False

    def getMeat(self, command):
        meat = ""
        meat = command.strip("{c>")
        meat = meat.strip("}")
        return meat

    def defineMeat(self, meat):
        if(meat.startswith("M")):
            # motor related command
            if(meat == "M?"):
                return Cmds.GetAllMotorStatuses
            elif(len(meat) == 3 and meat.endswith("?")):
                return Cmds.GetSingleMotorStatus
            elif(len(meat) >= 4 and meat.find(";") == 2):
                # specific motor status?
                splitMeat = meat.split(';')
                print("\tSet motor " + splitMeat[0][1] + " to speed " + splitMeat[1])
                return Cmds.SetMotorSpeed
            else:
                return Cmds.Invalid



## testing
# parser = CmdParser()
# 
# print(parser.parseCommand("c>M?"))
# print(parser.parseCommand("{c>M?}"))
# print(parser.parseCommand("{c>M1?}"))
# print(parser.parseCommand("{c>M1;233}"))
# print(parser.parseCommand("{c>M12;233}"))
