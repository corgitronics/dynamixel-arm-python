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


class CaseType:
    """Defines a type of case, such as 9mm.
    The machine determines the case type based upon height.  This defines a given cardridge type using a height range.  Any case measured that falls within this range is assumed to be of this type.
    The machine will carry the case to the appropriate bin and drop it.  This class also defines the position the case should be dropped at.
    """

    def __init__(self, code, name, label, labelPos, minHeight, maxHeight, minD, maxD, dropPosition):
        self.code = code  # an enum or constant that uniquely identifies this case type
        self.name = name
        self.label = label  # what to print on the display
        self.labelPos = labelPos  # what position to print the label
        self.minHeight = minHeight
        self.maxHeight = maxHeight
        self.minDiameter = minD
        self.maxDiameter = maxD
        self.dropPosition = dropPosition
        self.caseCount = 0

    def toString(self):
        print("name: {}, {}, {}, {}, {}, {}".format(self.name, self.minHeight, self.maxHeight, self.minDiameter, self.maxDiameter, self.dropPosition))





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

# -- build the list of case types
a9mmCase = CaseType(1, '9mm', '9mm', 0, 18.4, 19.5, 1)
a40swCase = CaseType(2, '40 S&W', '40sw', 5, 20.9, 22.0, 2)
a45Case = CaseType(3, '45 ACP', '45acp', 10, 22.1, 23.5, 3)
a10mmCase = CaseType(4, '10mm', '10mm', 99, 24.5, 25.5, 4)
a380Case = CaseType(5, '380 ACP', '380', 16, 16.9, 17.8, 5)
tallCase = CaseType(6, 'Over Height','Tall', 99, 25.51,99.0, 6)
junkCase = CaseType(7, 'Junk', 'Junk', 99, 0, 16.9, 6)

caseList.append(a9mmCase)
caseList.append(a40swCase)
caseList.append(a45Case)
caseList.append(a10mmCase)
# caseList.append(a380Case)
caseList.append(tallCase)
caseList.append(junkCase)

while True:
    time.sleep(0.1)
    pass

# arm.shutdown()
