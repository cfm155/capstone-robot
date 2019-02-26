#!/usr/bin/python
from ev3dev.ev3 import *
from threading import Thread

def Scan():
	global objectSpotted
	ir = InfraredSensor()
	eyeMotor = LargeMotor('outC')
	objectSpotted = False
	dir = 175
	eyeMotor.run_to_rel_pos(position_sp=dir, speed_sp=75, stop_action="brake")
	while(objectSpotted == False):
		eyeMotor.stop()
		distance = ir.value()
		if(ir.value() < 30):
			objectSpotted = True
			eyeMotor.stop()
			print("spotted")
		dir *= -1
		sleep(0.1)
	Scan()

def Slap():
	slapMotor = LargeMotor('outA')
	slapMotor.run_to_rel_pos(position_sp=180, speed_sp=1000, stop_action="hold")
	slapMotor.wait_while('running')
	slapMotor.run_to_rel_pos(position_sp=-180, speed_sp=1000, stop_action="hold")

global objectSpotted
objectSpotted = False
while(objectSpotted == False) :
	Scan()
Slap()
