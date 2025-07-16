import os
import sys
import time
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrStreamingServices

rvr = SpheroRvrObserver()

current_colour = "floor"
previous_colour = "floor"
speed = 16

url = 'https://192.168.12.1:3000/car/colour'

def color_detected_handler(color_detected_data):
    global current_colour, previous_colour, speed, url
    print('Color detection data response: ', color_detected_data)
    r = color_detected_data['ColorDetection']['R']
    g = color_detected_data['ColorDetection']['G']
    b = color_detected_data['ColorDetection']['B']

    if (r > 200 and g > 200 and b > 200):
        current_colour = "white";
        myobj = { 'colour': 'white'}
        requests.post(url, json = myobj)
    elif g > 230:
        print("Detected color: Tennis Ball")
        current_colour = "tennis ball"
        myobj = { 'colour': 'green'}
        requests.post(url, json = myobj)
    elif r > 230:
        print("Detected color: Neon Pink")
        current_colour = "neon pink"
        myobj = { 'colour': 'pink'}
        requests.post(url, json = myobj)
    else:
        print("Detected color: Floor")
        current_colour = "floor"

    print("Current color:", current_colour)
    print("Previous color:", previous_colour)
    if current_colour == "tennis ball":
        previous_colour = current_colour
        rvr.drive_rc_si_units(
            linear_velocity=.1,
            yaw_angular_velocity=120,
            flags=0
        )
    elif current_colour == "neon pink":
        previous_colour = current_colour
        rvr.drive_rc_si_units(
            linear_velocity=.1,
            yaw_angular_velocity=-120,
            flags=0
        )
    elif current_colour == "white":
        previous_colour = current_colour
        print('speed boost')
        rvr.drive_tank_normalized(
                left_velocity=32,  # Valid velocity values are [-127..127]
                right_velocity=32  # Valid velocity values are [-127..127]
        )
        speed = 32
    else:
        print('continue driving')
        rvr.drive_tank_normalized(
                left_velocity=speed,  # Valid velocity values are [-127..127]
                right_velocity=speed  # Valid velocity values are [-127..127]
        )

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
