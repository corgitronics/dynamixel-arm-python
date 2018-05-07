#!/usr/bin/env python3
#
#  Basic functions for a robot arm
#

# from pyax12.connection import Connection
# import pyax12.packet as pk
# import pyax12.utils as utils
import time
import arm2 as arm

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Define the pins
LEARN_BUTTON = 8
NEXT_BUTTON = 7
POSITION_1 = 12
POSITION_2 = 16
POSITION_3 = 20
POSITION_4 = 21


# Setup the pins
GPIO.setup(LEARN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(POSITION_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(POSITION_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(POSITION_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(POSITION_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


learnMode = False

arm.initialize()

def learn_callback(channel):
    print("* Learn Mode")
    global learnMode
    learnMode = True
    arm.freeMovement()

# When button 1 is pressed, either learn this position or goto the previously learned postion
def position1_callback(channel):
    global learnMode
    if learnMode is True:
        print("+ learning position 1")
        arm.recordPosition("one")
        arm.holdCurrentPosition()
        arm.resumeTorque()
        learnMode = False
    else:
        print("- moving to position 1")
        arm.gotoPosition("one")

# When button 2 is pressed, either learn this position or goto the previously learned postion
def position2_callback(channel):
    global learnMode
    if learnMode is True:
        print("+ learning position 2")
        arm.recordPosition("two")
        arm.holdCurrentPosition()
        arm.resumeTorque()
        learnMode = False
    else:
        print("- moving to position 2")
        arm.gotoPosition("two")

# When button 3 is pressed, either learn this position or goto the previously learned postion
def position3_callback(channel):
    global learnMode
    if learnMode is True:
        print("+ learning position 3")
        arm.recordPosition("three")
        arm.holdCurrentPosition()
        arm.resumeTorque()
        learnMode = False
    else:
        print("- moving to position 3")
        arm.gotoPosition("three")

# When button 4 is pressed, either learn this position or goto the previously learned postion
def position4_callback(channel):
    global learnMode
    if learnMode is True:
        print("+ learning position 4")
        arm.recordPosition("four")
        arm.holdCurrentPosition()
        arm.resumeTorque()
        learnMode = False
    else:
        print("- moving to position 4")
        arm.gotoPosition("four")


# Define events for the buttons
GPIO.add_event_detect(LEARN_BUTTON, GPIO.FALLING, callback=learn_callback, bouncetime=300)
# GPIO.add_event_detect(NEXT_BUTTON, GPIO.FALLING, callback=next_callback, bouncetime=300)
GPIO.add_event_detect(POSITION_1, GPIO.FALLING, callback=position1_callback, bouncetime=300)
GPIO.add_event_detect(POSITION_2, GPIO.FALLING, callback=position2_callback, bouncetime=300)
GPIO.add_event_detect(POSITION_3, GPIO.FALLING, callback=position3_callback, bouncetime=300)
GPIO.add_event_detect(POSITION_4, GPIO.FALLING, callback=position4_callback, bouncetime=300)

while True:
    time.sleep(0.1)
    pass

# arm.shutdown()
