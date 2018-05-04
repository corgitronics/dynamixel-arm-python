#!/usr/bin/env python3
#
#  Basic functions for a robot arm
#

from pyax12.connection import Connection
import time
import RPi.GPIO as GPIO
import pyax12.packet as pk
import pyax12.utils as utils
import arm2 as arm

arm.initialize()

arm.openGripper()
time.sleep(2)
arm.closeGripper()

arm.shutdown()
