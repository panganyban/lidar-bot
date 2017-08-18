# LIDAR PROJECT
## SJSU CMPE 220 Spring 2016

> Elton L., James G., Eric P., Andrew V.

## Overview

This repo is being used to keep track of the development of the communication system between the lidar controller and IO controller.

Goal is to abstract motor control from lidar processing. 

### Methods used

* `python2.7` used
* (TCP) for communication
* Client-Server architecture
    * Server reads lidar data streams and controls IO 
        * Two threads
            * Server thread -- listens to incoming TCP connections and puts data streams into buffer (queue)
            * Processing thread -- processes the data in the buffer
    * Client module can be used to communicate with server 
        * Lidar streams the data into the server to process and control motors


## Folder Structure

* Folder structure below shows all directories and important files

```
/reporoot
    /Adafruit                 # contains drivers for i2c dc motor hat
    /avoided                  # production code for project
        /client               # contains the lidar streamer
            ioclient.py       # small class to connect and stream to server
            lidarClient.py    # client that streams lidar data to server
            rplidar.py        # RPLidar python module by SkRobo
        /controller           # contains the controller code
            central.py        # server code for receiving lidar tcp stream
            LidarProcessor.py # processing code for lidar data
    /remotecontrol            # remote control library using nodejs
        /node_modules         # modules required for remote control
        index.js              # main file. run with: `node index.js ipaddr`
        package.json          # package info
    /experimental             # contains experimental code during development
        /python             
            /central          # original central server files -- oudated (see above)
            /lidarstreamer    # original lidar streamer -- outdated (see above)
            /udp              # udp method -- unused
            /uds              # uds method -- unused
```

## Resources

* [rpLidar.py by SkyRobo](https://github.com/SkRobo/rplidar)
* [Adafruit Motor HAT Python Library](https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library)