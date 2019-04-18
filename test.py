#!/usr/bin/env python3
# Password: maker
from ev3dev.ev3 import *
from time import sleep
# V2/V1 = (R + r)/(R - r)
turn = 150
mA = LargeMotor('outA')
mB = LargeMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')
command = 'g'
while(command != 'x'):
	command = input("command: ")
	if(command == 'f'):
		mA.run_timed(time_sp=1000, speed_sp=600)
		mB.run_timed(time_sp=1000, speed_sp=-600)
		mC.run_timed(time_sp=1000, speed_sp=-600)
		mD.run_timed(time_sp=1000, speed_sp=600)
	elif(command == 'r'):
		mA.run_timed(time_sp=1000, speed_sp=450 + turn)
		mB.run_timed(time_sp=1000, speed_sp=-450 - turn)
		mC.run_timed(time_sp=1000, speed_sp=-450 + turn)
		mD.run_timed(time_sp=1000, speed_sp=450 - turn)
	elif(command == 'l'):
		mA.run_timed(time_sp=1000, speed_sp=450 - turn)
		mB.run_timed(time_sp=1000, speed_sp=-450 + turn)
		mC.run_timed(time_sp=1000, speed_sp=-450 - turn)
		mD.run_timed(time_sp=1000, speed_sp=450 + turn)
	elif(command == 'v'):
		mA.run_timed(time_sp=1000, speed_sp=-600)
		mB.run_timed(time_sp=1000, speed_sp=600)
		mC.run_timed(time_sp=1000, speed_sp=600)
		mD.run_timed(time_sp=1000, speed_sp=-600)
#print("set speed (speed_sp) = " + str(mA.speed_sp))
#sleep(1)  # it takes a moment for the motor to start moving
#print("actual speed = " + str(mA.speed))
#sleep(2)