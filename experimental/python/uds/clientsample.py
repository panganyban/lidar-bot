#!/usr/bin/env python3

import ioclient

udsClient = ioclient.IOClient

if __name__ == '__main__':
    udsClient = ioclient.IOClient()
    if udsClient.connect():
        response = udsClient.sendCommand("M?")
        print(response + "\n")
        response = udsClient.sendCommand("M2;100")
        print(response + "\n")
        response = udsClient.sendCommand("M1;25")
        print(response + "\n")
        response = udsClient.sendCommand("M?")
        print(response + "\n")
    else:
        print("Unable to connect")

