#!/usr/bin/env python3
# Password: maker
from ev3dev.ev3 import *
from time import sleep
mA = LargeMotor('outA')
mD = LargeMotor('outD')
command = 'g'
while(command != 'x'):
	command = getch("command: ")
	if(command == 'f'):
		mA.run_timed(time_sp=1000, speed_sp=750)
		mD.run_timed(time_sp=1000, speed_sp=750)
	elif(command == 'r'):
		mD.run_timed(time_sp=1000, speed_sp=750)
	elif(command == 'l'):
		mA.run_timed(time_sp=1000, speed_sp=750)
	elif(command == 'v'):
		mA.run_timed(time_sp=1000, speed_sp=-750)
		mD.run_timed(time_sp=1000, speed_sp=-750)
#print("set speed (speed_sp) = " + str(mA.speed_sp))
#sleep(1)  # it takes a moment for the motor to start moving
#print("actual speed = " + str(mA.speed))
#sleep(2)