#!/usr/bin/env python3
from ev3dev.ev3 import *

# stop all the motors so that the robot does not go out of control
mA = LargeMotor('outA')
mB = LargeMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')
mA.stop(stop_action="hold")
mB.stop(stop_action="hold")
mC.stop(stop_action="hold")
mD.stop(stop_action="hold")