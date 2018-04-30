#!/usr/bin/env python3

from pyax12.connection import Connection
import time
import RPi.GPIO as GPIO
import pyax12.packet as pk
import pyax12.utils as utils

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

port = '/dev/ttyACM0'
baudrate = 1000000
timeout = 2000
tx_rx = 18

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


def initConnection():
    return(Connection(port=port,
                                   baudrate=baudrate,
                                   timeout=timeout,
                                   rpi_gpio=tx_rx))


serial_connection = initConnection()


# defines the basic settings for a servo and provides basic actions
#   provides some safe defaults, in case those are forgotten
class Servo:
    def __init__(self, name, id, cw_imit=90, ccw_limit=90, torque=150, speed=150):
        self.name = name
        self.id = id
        self.cw_limit = cw_imit
        self.ccw_limit = ccw_limit
        self.max_torque = torque
        self.speed = speed
        setMaxTorque(self.id, self.max_torque)
        setCW(self.id, self.cw_limit)
        setCCW(self.id, self.ccw_limit)
        setSpeed(self.id, self.speed)

# answer this servo's current settings
    def toString(self):
        print("name: {}, ID {}, CW {}, CCW {}, Torque {}, Speed{}".format(self.name,self.id, self.cw_limit, self.ccw_limit, self.max_torque, self.speed))

# answer this servo'c current position
    def currentPosition(self):
        serial_connection.get_present_position(self.id)

# set the position, default to the servo's preset speed and torque
    def goto(self, position, speed=0):
        if (speed == 0):
            speed = self.speed
        serial_connection.goto(self.id, position, speed, False)


def setMaxTorque(dynamixel_id, maxT):
    params = utils.int_to_little_endian_bytes(maxT)
    serial_connection.write_data(dynamixel_id, pk.MAX_TORQUE, params)

def setCW(dynamixel_id,cw):
    global serial_connection
    serial_connection.set_cw_angle_limit(dynamixel_id, cw)

def setCCW(dynamixel_id,ccw):
    global serial_connection
    serial_connection.set_ccw_angle_limit(dynamixel_id, ccw)

def setSpeed(dynamixel_id, speed):
    global serial_connection
    serial_connection.set_speed(dynamixel_id, speed)

def openGripper():
    gripper.goto(gripper_ccw)

def closeGripper():
    gripper.goto(gripper_cw)



shoulder = Servo("Shoulder", shoulder_id, shoulder_cw, shoulder_ccw, shoulder_torque, shoulder_speed)
elbow = Servo("Elbow", elbow_id, elbow_cw, elbow_ccw, elbow_torque, elbow_speed)
gripper = Servo('Gripper', gripper_id, gripper_cw, gripper_ccw, gripper_torque, gripper_speed)

openGripper()
time.sleep(2)
closeGripper()

# Close the serial connection
serial_connection.close()
