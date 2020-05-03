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

    def __init__(self, bus):
        self._dev = i2c_device.I2CDevice(bus, 0x27)

    def read(self):
        # Start reading; send write without any data.
        self._dev.write(bytearray(0))


        status = 1
        bytes_read = bytearray(4)

        while status != 0:
            time.sleep(0.01)
            self._dev.readinto(bytes_read)
            status = (bytes_read[0] & 0xC0) >> 6

        humidity = ((bytes_read[0] & 0x3F) << 8) | (bytes_read[1])
        humidity = (humidity / ((1<<14) - 2))

        temperature = (bytes_read[2] << 6) | (bytes_read[3] >> 2)
        temperature = (temperature / ((1<<14) - 2)) * 165 - 40

        return humidity, temperature


if __name__ == "__main__":
    bus = busio.I2C(board.SCL, board.SDA)

    sensor = HIH6130(bus)

    humidity, temperature = sensor.read()
    print("Humidity: {:.2f} %RH".format(humidity * 100.0))
    print("Temperature: {:.2f} C".format(temperature))
