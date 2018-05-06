#!/usr/bin/env python3

from pyax12.connection import Connection
import time
import RPi.GPIO as GPIO
import pyax12.packet as pk

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

port = '/dev/ttyACM0'
baudrate = 1000000
timeout = 2000
tx_rx = 18

dynamixel_id = 3

serial_connection = Connection(port=port,
                                   baudrate=baudrate,
                                   timeout=timeout,
                                   rpi_gpio=tx_rx)

# Switch ON the LED
serial_connection.write_data(dynamixel_id, pk.LED, 1)

# Wait 2 seconds
time.sleep(2)

# Switch OFF the LED
serial_connection.write_data(dynamixel_id, pk.LED, 0)

# Wait 2 seconds
time.sleep(2)

# Switch ON the LED
serial_connection.write_data(dynamixel_id, pk.LED, 1)

# Wait 2 seconds
time.sleep(2)

# Switch OFF the LED
serial_connection.write_data(dynamixel_id, pk.LED, 0)

serial_connection.get_present_temperature(dynamixel_id)

# Close the serial connection
serial_connection.close()
