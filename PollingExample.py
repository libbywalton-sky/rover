#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './sphero-sdk-raspberrypi-python')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './Gamepad')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum

# Load the gamepad and time libraries
import Gamepad
import time

# Set up rover
rvr = SpheroRvrObserver()

# Gamepad settings
gamepadType = Gamepad.XboxONE
buttonHappy = 'CROSS'
buttonBeep = 'CIRCLE'
buttonExit = 'PS'
leftSpeed = 'LAS -Y'
rightSpeed = 'RAS -Y'

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# How fast?
speedMultiplier = 32
# Set some initial state
speed = 0.0
steering = 0.0


try:
    rvr.wake()
    # Give RVR time to wake up
    print('Waiting for rover to wake... 2 secs...')
    time.sleep(2)

    rvr.reset_yaw()


    #rvr.drive_tank_normalized(
    #    left_velocity=16,  # Valid velocity values are [-127..127]
    #    right_velocity=16  # Valid velocity values are [-127..127]
    #)

    #time.sleep(2)

    #rvr.drive_tank_normalized(
        #left_velocity=0,  # Valid velocity values are [-127..127]
        #right_velocity=0  # Valid velocity values are [-127..127]
    #)

    print('Ready for gamepad input!')

    # Handle joystick updates one at a time
    while gamepad.isConnected():
        # Wait for the next event
        eventType, control, value = gamepad.getNextEvent()

        # Determine the type
        if eventType == 'BUTTON':
            # Button changed
            if control == buttonHappy:
                # Happy button (event on press and release)
                if value:
                    print(':)')
                else:
                    print(':(')
            elif control == buttonBeep:
                # Beep button (event on press)
                if value:
                    print('BEEP')
            elif control == buttonExit:
                # Exit button (event on press)
                if value:
                    print('EXIT')
                    break
        elif eventType == 'AXIS':
            # Joystick changed
            if control == leftSpeed:
                # Left tread
                speed = -value
            elif control == rightSpeed:
                # Right tread
                steering = -value

            print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))
            
            rvr.drive_tank_normalized(
                left_velocity=round(speed * speedMultiplier),  # Valid velocity values are [-127..127]
                right_velocity=round(steering * speedMultiplier)  # Valid velocity values are [-127..127]
            )

except KeyboardInterrupt:
    print('\nProgram terminated with keyboard interrupt.')

finally:
    rvr.close()
