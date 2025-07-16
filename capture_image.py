#!/usr/bin/python3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './picamera2')))

from picamera2 import Picamera2

import time
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1536, 864)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start()
time.sleep(2)

while True:
	picam2.capture_file("test.jpg")
	time.sleep(1)
