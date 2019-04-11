#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
mC = LargeMotor('outC')
# Connect infrared and touch sensors to any sensor ports
ir = InfraredSensor() 
# Put the infrared sensor into proximity mode.
mC.run_timed(time_sp=1000, speed_sp=750)
