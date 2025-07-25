import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './sphero-sdk-raspberrypi-python')))
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

import time
import signal

import pytesseract

from picamera2 import MappedArray, Picamera2


rvr = SpheroRvrObserver()


def main():

    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration({"size": (1024, 768)}))
    #picam2.start_preview(Preview.QTGL)
    picam2.start()

    threshold = 50

    print("starting rover")
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    current_command = "stop"

    while True:
        print("doing text detection")
        array = picam2.capture_array()
        print("Captured image array")
        data = [line.split('\t') for line in pytesseract.image_to_data(array).split('\n')][1:-1]
        print("retrived data")
        data = [{"text": item[11], "conf": int(item[10]), "box": (item[6], item[7], item[8], item[9])} for item in data]
        data = [item for item in data if item["conf"] > threshold and not item["text"].isspace()]
        print("Detected data:", data)
        for item in data:
            item["box"] = tuple(map(int, item["box"]))
            text = item["text"].lower()
            print("Detected text:", text)
            if "go" in text:
                current_command = "go"
            elif "stop" in text:
                current_command = "stop"
                
        print("Current command:", current_command)
        if current_command == "go":
            print("RVR moving forward")
            rvr.drive_tank_normalized(
                left_velocity=16,  # Valid velocity values are [-127..127]
                right_velocity=16  # Valid velocity values are [-127..127]
            )
        elif current_command == "stop":
            print("RVR stopping")
            rvr.drive_tank_normalized(
                left_velocity=0,  # Valid velocity values are [-127..127]
                right_velocity=0  # Valid velocity values are [-127..127]
            )

    """
    # Init the rover
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()


        for x in range(drive_count):
            rvr.drive_tank_normalized(
                left_velocity=16,  # Valid velocity values are [-127..127]
                right_velocity=16  # Valid velocity values are [-127..127]
            )

            time.sleep(2)

        rvr.drive_tank_normalized(
            left_velocity=0,  # Valid velocity values are [-127..127]
            right_velocity=0  # Valid velocity values are [-127..127]
        )

        time.sleep(2)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()
    """


if __name__ == '__main__':
    main()
