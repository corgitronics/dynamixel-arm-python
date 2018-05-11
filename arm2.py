#!/usr/bin/env python3
#
#  Basic functions for a robot arm
#

from pyax12.connection import Connection
import time
import jsonpickle
import RPi.GPIO as GPIO
import pyax12.packet as pk
import pyax12.utils as utils

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

serial_connection = None

port = '/dev/ttyACM0'
baudrate = 1000000
timeout = 20
tx_rx = 18

positionsFile = "positions.js"

# Shoulder settings
shoulder_id = 2
shoulder_cw = 190
shoulder_ccw = 810
shoulder_torque = 150
shoulder_speed = 400

# Elbow settings
elbow_id = 3
elbow_cw = 25
elbow_ccw = 980
elbow_torque = 150
elbow_speed = 500

#Gripper settings
gripper_id = 4
gripper_cw = 304
gripper_ccw = 774
gripper_torque = 150
gripper_speed = 200

positionList = {}
shoulder = None
elbow = None


def initConnection():
    return(Connection(port=port,
                       baudrate=baudrate,
                       timeout=timeout,
                       rpi_gpio=tx_rx))

# defines a set of servo angles that combine to put the arm in a particular position
class Position(object):
    def __init__(self, pos1, pos2):
        self.shoulderPosition = pos1
        self.elbowPosition = pos2



# defines the basic settings for a servo and provides basic actions
#   provides some safe defaults, in case those are forgotten
class Servo:
    def __init__(self, name, id, cw_imit=90, ccw_limit=90, torque=150, torqueLimit=150, speed=150):
        self.name = name
        self.id = id
        self.cw_limit = cw_imit
        self.ccw_limit = ccw_limit
        self.speed = speed
        self.max_torque = torque
        self.torque_limit = torqueLimit
        self.setMaxTorque(self.max_torque)
        self.setTorqueLimit(torqueLimit)
        self.setCW(self.cw_limit)
        self.setCCW(self.ccw_limit)
        self.setSpeed(self.speed)
        self.goalPosition = 0

# answer this servo's current settings
    def toString(self):
        print("name: {}, ID:{}, CW:{}, CCW:{}, Torque:{}, Speed:{}, Goal Position:{}".format(self.name,self.id, self.cw_limit, self.ccw_limit, self.max_torque, self.speed, self.goalPosition))

# answer this servo's current position
    def currentPosition(self):
        return serial_connection.get_present_position(self.id)

# set the position, default to the servo's preset speed and torque
    def goto(self, position, speed=0):
        self.goalPosition = position
        if (speed == 0):
            speed = self.speed
        serial_connection.goto(self.id, position, speed, False)

    def setMaxTorque(self, maxT):
        self.max_torque = maxT
        params = utils.int_to_little_endian_bytes(maxT)
        serial_connection.write_data(self.id, pk.MAX_TORQUE, params)

    def setTorqueLimit(self, maxT):
        self.torque_limit = maxT
        params = utils.int_to_little_endian_bytes(maxT)
        serial_connection.write_data(self.id, pk.TORQUE_LIMIT, params)

    def setCW(self, cw):
        global serial_connection
        serial_connection.set_cw_angle_limit(self.id, cw)

    def setCCW(self, ccw):
        global serial_connection
        serial_connection.set_ccw_angle_limit(self.id, ccw)

    def setSpeed(self, speed):
        global serial_connection
        serial_connection.set_speed(self.id, speed)

    def isAtGoalPosition(self):
        return self.goalPosition - 4 <= self.currentPosition() <= self.goalPosition + 4

    def freeMovement(self):
        params = utils.int_to_little_endian_bytes(0)
        serial_connection.write_data(self.id, pk.MAX_TORQUE, params)
        serial_connection.write_data(self.id, pk.TORQUE_LIMIT, params)

    def resumeTorque(self):
        params = utils.int_to_little_endian_bytes(self.max_torque)
        serial_connection.write_data(self.id, pk.TORQUE_LIMIT, params)
        params = utils.int_to_little_endian_bytes(self.torque_limit)
        serial_connection.write_data(self.id, pk.MAX_TORQUE, params)

    def holdCurrentPosition(self):
        aPosition = self.currentPosition()
        self.goto(aPosition, 150)


def isAtGoalPosition():
    global shoulder
    global elbow
    return shoulder.isAtGoalPosition() and elbow.isAtGoalPosition()


def recordPosition(name):
    global positionList
    global shoulder
    global elbow
    aPosition = Position(shoulder.currentPosition(), elbow.currentPosition())
    positionList.update({name: aPosition})
    f = open(positionsFile, 'w')
    json_obj = jsonpickle.encode(positionList)
    f.write(json_obj)

def gotoPosition(name):
    global positionList
    global shoulder
    global elbow
    aPosition = positionList[name]
    shoulder.goto(aPosition.shoulderPosition, 50)
    elbow.goto(aPosition.elbowPosition, 150)

def holdCurrentPosition():
    global shoulder
    global elbow
    shoulder.holdCurrentPosition()
    elbow.holdCurrentPosition()

def freeMovement():
    global shoulder
    global elbow
    shoulder.freeMovement()
    elbow.freeMovement()

def resumeTorque():
    global shoulder
    global elbow
    shoulder.resumeTorque()
    elbow.resumeTorque()

def openGripper():
    gripper.goto(gripper_ccw)

def closeGripper():
    gripper.goto(gripper_cw)

def initialize():
    global serial_connection
    global shoulder
    global elbow
    global gripper
    global positionList
    serial_connection = initConnection()
    shoulder = Servo("shoulder", shoulder_id, shoulder_cw, shoulder_ccw, shoulder_torque, shoulder_speed)
    elbow = Servo("elbow", elbow_id, elbow_cw, elbow_ccw, elbow_torque, elbow_speed)
    gripper = Servo("gripper", gripper_id, gripper_cw, gripper_ccw, gripper_torque, gripper_speed)
    try:
        with open(positionsFile) as json_data:
            json_str = json_data.read()
            positionList = jsonpickle.decode(json_str)
            json_data.close()
    except:
        print("no positions file: {}".format(positionsFile))

def shutdown():
    global serial_connection
    serial_connection.close()




