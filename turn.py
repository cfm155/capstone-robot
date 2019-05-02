#!/usr/bin/env python3
# Password: maker
from ev3dev.ev3 import *
from time import sleep
# V2/V1 = (R + r)/(R - r)
turn = 100
speed = 150
mA = LargeMotor('outA')
mB = LargeMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')
mA.stop(stop_action="hold")
mB.stop(stop_action="hold")
mC.stop(stop_action="hold")
mD.stop(stop_action="hold")
command = 'g'
print("beginning turn")

mA.run_timed(time_sp=3000, speed_sp=speed + turn)
mB.run_timed(time_sp=3000, speed_sp=-speed - turn)
mC.run_timed(time_sp=3000, speed_sp=-speed + turn)
mD.run_timed(time_sp=3000, speed_sp=speed - turn)
print("finished turn")
#print("set speed (speed_sp) = " + str(mA.speed_sp))
#sleep(1)  # it takes a moment for the motor to start moving
#print("actual speed = " + str(mA.speed))
#sleep(2)