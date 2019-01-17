# dynamixel-arm-python
Using Dynamixel AX-12A servos for a simple robotic arm.

This code supports the video demo on Youtube:  https://youtu.be/M20P-k8dF4g

This software leverages a couple of other libraries, so you'll also need:
* RPi.GPIO `sudo apt-get -y install python-dev python3-rpi.gpio`
* jsonpickle - https://github.com/jsonpickle
* pyax12 - https://github.com/jeremiedecock/pyax12

_( according to my commit comments, these should be fully functioning versions)_

## machine.py 
* basic arm movements
* can learn and playback positions using buttons

## machine2.py
* Learns positions
* Determines case type based on diameter
* Automatically grips and delivers case to correct position

## arm2.py 
* module to communicate with the arm
* a larger application like __machine.py__ calls functions in __arm2.py__
