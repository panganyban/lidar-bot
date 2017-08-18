#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
backRight = mh.getMotor(1)
frontRight = mh.getMotor(2)
frontLeft = mh.getMotor(3)
backLeft = mh.getMotor(4)

# used for calibrating motors
TURN_SPEED = 255
LEFT_SPEED = 200
RIGHT_SPEED = 200


def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)


def rotateRight():
    frontLeft.setSpeed(TURN_SPEED)
    backLeft.setSpeed(TURN_SPEED)
    frontRight.setSpeed(TURN_SPEED)
    backRight.setSpeed(TURN_SPEED)
    frontLeft.run(Adafruit_MotorHAT.FORWARD)
    backLeft.run(Adafruit_MotorHAT.FORWARD)
    frontRight.run(Adafruit_MotorHAT.BACKWARD)
    backRight.run(Adafruit_MotorHAT.BACKWARD)


def rotateLeft():
    frontLeft.setSpeed(TURN_SPEED)
    backLeft.setSpeed(TURN_SPEED)
    frontRight.setSpeed(TURN_SPEED)
    backRight.setSpeed(TURN_SPEED)
    frontRight.run(Adafruit_MotorHAT.FORWARD)
    backRight.run(Adafruit_MotorHAT.FORWARD)
    frontLeft.run(Adafruit_MotorHAT.BACKWARD)
    backLeft.run(Adafruit_MotorHAT.BACKWARD)


def turnRight(degree):
    frontLeft.setSpeed(LEFT_SPEED)
    backLeft.setSpeed(LEFT_SPEED)
    frontRight.setSpeed(RIGHT_SPEED)
    backRight.setSpeed(RIGHT_SPEED)
    frontLeft.run(Adafruit_MotorHAT.FORWARD)
    backLeft.run(Adafruit_MotorHAT.FORWARD)
    frontRight.run(Adafruit_MotorHAT.BACKWARD)
    backRight.run(Adafruit_MotorHAT.BACKWARD)
    sleepTime = degree * 1.00 / 90
    time.sleep(sleepTime)
    frontLeft.run(Adafruit_MotorHAT.RELEASE)
    backLeft.run(Adafruit_MotorHAT.RELEASE)
    frontRight.run(Adafruit_MotorHAT.RELEASE)
    backRight.run(Adafruit_MotorHAT.RELEASE)


def turnLeft(degree):
    frontLeft.setSpeed(LEFT_SPEED)
    backLeft.setSpeed(LEFT_SPEED)
    frontRight.setSpeed(RIGHT_SPEED)
    backRight.setSpeed(RIGHT_SPEED)
    frontRight.run(Adafruit_MotorHAT.FORWARD)
    backRight.run(Adafruit_MotorHAT.FORWARD)
    frontLeft.run(Adafruit_MotorHAT.BACKWARD)
    backLeft.run(Adafruit_MotorHAT.BACKWARD)
    sleepTime = degree * 1.20 / 90
    time.sleep(sleepTime)
    frontRight.run(Adafruit_MotorHAT.RELEASE)
    backRight.run(Adafruit_MotorHAT.RELEASE)
    frontLeft.run(Adafruit_MotorHAT.RELEASE)
    backLeft.run(Adafruit_MotorHAT.RELEASE)


def moveForward(distance):
    frontLeft.setSpeed(LEFT_SPEED)
    frontRight.setSpeed(RIGHT_SPEED)
    backLeft.setSpeed(LEFT_SPEED)
    backRight.setSpeed(RIGHT_SPEED)
    frontLeft.run(Adafruit_MotorHAT.FORWARD)
    frontRight.run(Adafruit_MotorHAT.FORWARD)
    backRight.run(Adafruit_MotorHAT.FORWARD)
    backLeft.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(distance)  # time = distance * x/scale
    frontLeft.run(Adafruit_MotorHAT.RELEASE)
    frontRight.run(Adafruit_MotorHAT.RELEASE)
    backLeft.run(Adafruit_MotorHAT.RELEASE)
    backRight.run(Adafruit_MotorHAT.RELEASE)


def goForward():
    frontLeft.setSpeed(LEFT_SPEED)
    frontRight.setSpeed(RIGHT_SPEED)
    backLeft.setSpeed(LEFT_SPEED)
    backRight.setSpeed(RIGHT_SPEED)
    frontLeft.run(Adafruit_MotorHAT.FORWARD)
    frontRight.run(Adafruit_MotorHAT.FORWARD)
    backRight.run(Adafruit_MotorHAT.FORWARD)
    backLeft.run(Adafruit_MotorHAT.FORWARD)


def moveBackward(distance):
    frontLeft.setSpeed(LEFT_SPEED)
    frontRight.setSpeed(RIGHT_SPEED)
    backLeft.setSpeed(LEFT_SPEED)
    backRight.setSpeed(RIGHT_SPEED)
    frontLeft.run(Adafruit_MotorHAT.BACKWARD)
    frontRight.run(Adafruit_MotorHAT.BACKWARD)
    backRight.run(Adafruit_MotorHAT.BACKWARD)
    backLeft.run(Adafruit_MotorHAT.BACKWARD)
    time.sleep(distance)  # time = distance * x/scale
    frontLeft.run(Adafruit_MotorHAT.RELEASE)
    frontRight.run(Adafruit_MotorHAT.RELEASE)
    backLeft.run(Adafruit_MotorHAT.RELEASE)
    backRight.run(Adafruit_MotorHAT.RELEASE)


def goBackward():
    frontLeft.setSpeed(LEFT_SPEED)
    frontRight.setSpeed(RIGHT_SPEED)
    backLeft.setSpeed(LEFT_SPEED)
    backRight.setSpeed(RIGHT_SPEED)
    frontLeft.run(Adafruit_MotorHAT.BACKWARD)
    frontRight.run(Adafruit_MotorHAT.BACKWARD)
    backRight.run(Adafruit_MotorHAT.BACKWARD)
    backLeft.run(Adafruit_MotorHAT.BACKWARD)
