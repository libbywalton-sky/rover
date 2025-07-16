from sphero_sdk import SpheroRvrObserver
from xbox360controller import Xbox360Controller
import os
import sys
import time
import signal
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../')))


rvr = SpheroRvrObserver()


def main():
    # Init the rover
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()

        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            while True:
                print(round(controller.axis_l.y * 2) / 2)
    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()

        # # drive forward, 50% speed
        # rvr.drive_tank_normalized(
        #     left_velocity=16,  # Valid velocity values are [-127..127]
        #     right_velocity=16  # Valid velocity values are [-127..127]
        # )

        # # Delay to allow RVR to drive
        # time.sleep(1)

        # rvr.drive_tank_normalized(
        #     left_velocity=0,  # Valid velocity values are [-127..127]
        #     right_velocity=0  # Valid velocity values are [-127..127]
        # )

        # # Delay to allow RVR to drive
        # time.sleep(1)


if __name__ == '__main__':
    main()
