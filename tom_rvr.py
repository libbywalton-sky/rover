import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './sphero-sdk-raspberrypi-python')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './Gamepad')))
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

from xbox360controller import Xbox360Controller
import time
import signal


rvr = SpheroRvrObserver()


def main():
    # Initial settings
    vleft = 0
    vright = 0

    # Init the rover
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()


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

        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            while True:
                #print(controller.axis_l.y)
                #vleft_new = round(controller.axis_l.y * 2) / 2
                vleft_new = round(controller.axis_l.y * 32)
                #print(vleft, vleft_new)

                if(vleft_new != vleft):
                    print("was", vleft, "now", vleft_new)
                    vleft = vleft_new

                    #rvr.drive_tank_normalized(
                        #left_velocity=vleft_new,  # Valid velocity values are [-127..127]
                        #right_velocity=0  # Valid velocity values are [-127..127]
                    #)
                #time.sleep(0.05)

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
