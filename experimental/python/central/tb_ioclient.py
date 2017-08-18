#!/usr/bin/env python
import sys
import ioclient

client = ioclient.IOClient()

client.connect()
i = 0
conOk = True
try:
    while(conOk is not False):
        """sendcommand returns:
        false - failure
        string - response (could be empty)
        """
        # timeout of 0 means don't wait for response
        conOk = client.sendCommand(" ".join(sys.argv[1:]) + str(i),
                                   timeout=0)
        i += 1
finally:
    print "finally"
    client.close()
