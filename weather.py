#!/usr/bin/env python3

import time
import board
import busio
from datetime import datetime

from hih6130 import HIH6130

from influxdb import InfluxDBClient

if __name__ == "__main__":
    bus = busio.I2C(board.SCL, board.SDA)

    sensor = HIH6130(bus)

    client = InfluxDBClient('arg', 8086, 'home_assistant', 'home_assistant', 'home_assistant')

    PERIOD = 1.0

    n = round(time.time())

    while True:
        n += PERIOD
        remain = n - time.time()
        print(remain)
        if remain > 0.0:
            time.sleep(remain)

        now = datetime.now()
        humidity, temperature = sensor.read()
        print(now.isoformat())
        data = [
            {
                "measurement": "train_shed",
                "time": now.isoformat(),
                "fields": {
                    "humidity": humidity * 100.0,
                    "temperature": temperature,
                }
            }
        ]
        client.write_points(data)



