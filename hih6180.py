#!/usr/bin/env python3
#
# Circuitpython driver (and program) for HIH-6180 sensor.
#
# Author: Austin Hendrix
#

import board
import busio

from micropython import const
import adafruit_bus_device.i2c_device as i2c_device

try:
    import struct
except ImportError:
    import ustruct as struct


class HIH6180(object):
    pass

if __name__ == "__main__":
    bus = busio.I2C(board.SCL, board.SDA)


    device = bus.I2CDevice(bus, 0x27)


