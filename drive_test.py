import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './sphero-sdk-raspberrypi-python')))
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

import time
import signal


rvr = SpheroRvrObserver()


def main():
    # Get number of times to run test
    drive_count = int(sys.argv[1]) if len(sys.argv) > 1 else 1 

    print(drive_count)
    print(sys.argv)

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

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()

if __name__ == '__main__':
    main()
