import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrStreamingServices

rvr = SpheroRvrObserver()

current_colour = "floor"
previous_colour = "floor"

def color_detected_handler(color_detected_data):
    print('Color detection data response: ', color_detected_data)
    r = color_detected_data['ColorDetection']['R']
    g = color_detected_data['ColorDetection']['G']
    b = color_detected_data['ColorDetection']['B']
    if g > 230:
        print("Detected color: Tennis Ball")
        current_colour = "tennis ball"
    elif r > 230:
        print("Detected color: Neon Pink")
        current_colour = "neon pink"
    elif b > 150:
        print("Detected color: Blue")
        current_colour = "blue"
    else:
        print("Detected color: Floor")
        current_colour = "floor"

    print("Current color:", current_colour)
    if previous_colour == current_colour:
        print("early return")
        return
    elif current_colour == "tennis ball":
        previous_colour = current_colour
        rvr.drive_rc_si_units(
            linear_velocity=.1,
            yaw_angular_velocity=90,
            flags=0
        )
    elif current_colour == "neon pink":
        previous_colour = current_colour
        rvr.drive_rc_si_units(
            linear_velocity=.1,
            yaw_angular_velocity=-90,
            flags=0
        )
    elif current_colour == "blue":
        previous_colour = current_colour
        print('speed boost')
    else:
        print('continue driving')
        




def main():
    """ This program demonstrates how to use the color sensor on RVR (located on the down side of RVR, facing the floor)
        to report colors detected.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.enable_color_detection(is_enabled=True)
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.color_detection,
            handler=color_detected_handler
        )
        rvr.sensor_control.start(interval=250)

        # Allow this program to run for 10 seconds
        time.sleep(60)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.sensor_control.clear()

        # Delay to allow RVR issue command before closing
        time.sleep(.5)
        
        rvr.close()


if __name__ == '__main__':
    main()
