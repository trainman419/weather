#!/usr/bin/env python3

import argparse
from datetime import datetime
import logging
import logging.handlers
import math
import sys
import time
import os

import board
import busio
import setproctitle

from hih6130 import HIH6130

from influxdb import InfluxDBClient

if __name__ == "__main__":
    setproctitle.setproctitle(os.path.basename(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-l", "--local", action="store_true", default=False,
            help="Skip logging to syslog")

    args = parser.parse_args()

    # Get root logger.
    STREAM_FMT = "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
    SYSLOG_FMT = "weather.py: %(levelname)s:%(name)s: %(message)s"
    log = logging.getLogger()

    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    if args.local:
        # Set up stream handler with custom format.
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(logging.Formatter(fmt=STREAM_FMT))
        log.addHandler(streamhandler)
    else:
        # Set root logger output to syslog with custom format.
        syslog_handler = logging.handlers.SysLogHandler(address = "/dev/log")
        syslog_handler.setFormatter(logging.Formatter(fmt=SYSLOG_FMT))
        log.addHandler(syslog_handler)
        log.debug("Logging to syslog")

    bus = busio.I2C(board.SCL, board.SDA)

    sensor = HIH6130(bus)

    client = InfluxDBClient('arg', 8086, 'home_assistant', 'home_assistant', 'home_assistant')

    PERIOD = 15.0

    n = math.ceil(time.time())

    startdelay = n - time.time()
    log.debug("Sleeping for %f at startup", startdelay)
    time.sleep(startdelay)

    while True:
        now = datetime.now()
        humidity, temperature = sensor.read()
        log.info("%.2f C, %.2f %%RH", temperature, humidity * 100)
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

        n += PERIOD
        remain = n - time.time()
        if remain > 0.0:
            log.debug("Sleeping for %.4f", remain)
            time.sleep(remain)
