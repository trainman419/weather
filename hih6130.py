#!/usr/bin/env python3
#
# Circuitpython driver (and program) for HIH-6130 sensor.
#
# Author: Austin Hendrix
#

import time
import board
import busio

from micropython import const
import adafruit_bus_device.i2c_device as i2c_device

try:
    import struct
except ImportError:
    import ustruct as struct


class HIH6130(object):
    pass

if __name__ == "__main__":
    bus = busio.I2C(board.SCL, board.SDA)

    device = i2c_device.I2CDevice(bus, 0x27)

    out = bytearray(0)

    device.write(out)

    time.sleep(0.1)

    bytes_read = bytearray(4)

    device.readinto(bytes_read)

    print("Raw data", bytes_read[0], bytes_read[1], bytes_read[2], bytes_read[3])

    status = (bytes_read[0] & 0xC0) >> 6
    print("Status", status)

    humidity = ((bytes_read[0] & 0x03) << 8) | (bytes_read[1])
    print(humidity, (1<<14))
    humidity = (humidity / ((1<<14) - 2))
    print("Humidity: {:.2f} %RH".format(humidity * 100.0))

    temperature = (bytes_read[2] << 6) | (bytes_read[3] >> 2)

    print(temperature)

    temperature = (temperature / ((1<<14) - 2)) * 165 - 40

    print("Temperature: {:.2f} C".format(temperature))

