#!/usr/bin/env python
import ioclient
from rplidar import RPLidar

client = ioclient.IOClient()
client.connect()
PORT_NAME = '/dev/tty.SLAB_USBtoUART'
# PORT_NAME = '/dev/ttyUSB0'


def run():
    lidar = RPLidar(PORT_NAME)
    try:
        print('Recording measurements.. Ctrl+C to stop')
        # prev_deg = 0.0
        deg = 0.0
        for scan in lidar.iter_measurments():
            if scan[1] > 0:
                # line = str(measurement[0]) + ', '
                # if scan[2] > prev_deg and scan[2] - prev_deg < 15\
                deg = scan[2]
                line = str(deg) + ","       # angle (Deg)
                line += str(scan[3]) + ";"   # distance (mm)
                # prev_deg = scan[2]
                if scan[1] > 3 and (scan[2] < 45 or scan[2] > 315):
                    if scan[3] < 500:
                        print str(deg) + " " + str(scan[3])

                if client.sendRawData(line, timeout=0) is False:
                    break
    except KeyboardInterrupt:
        print 'Stopping.'
        lidar.stop()
        lidar.reset()
        lidar.disconnect()
    finally:
        print "finally"
        client.close()


def runFake():
    msg = ""
    try:
        for i in xrange(359):
            msg = str(i) + "," + str(i / 2)
            client.sendRawData(msg, timeout=0)
            print i
    except KeyboardInterrupt:
        print "Stopping"
    finally:
        print "Closing client"
        client.close()

if __name__ == '__main__':
    # runFake()
    run()
