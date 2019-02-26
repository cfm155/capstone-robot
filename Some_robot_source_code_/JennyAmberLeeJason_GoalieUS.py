#!/usr/bin/env python3
from ev3dev.ev3 import *
import threading
import math
from time import sleep


def patrol(speed_sp=180):
	#Drive back and forth
	#speed
	Sound.speak('Crocodile go')

	while not BTN.any():
		sleep(1)
		Motor_Lock.acquire(True)

		RIGHT_MOTOR.run_forever(speed_sp = speed_sp)
		LEFT_MOTOR.run_forever(speed_sp = speed_sp)

		Motor_Lock.release()

def checkForEnemies():
	global SEEN_SOMEONE
	SEEN_SOMEONE = 0
	global IR
	IR.mode = 'US-DIST-CM'

	while True:
		sleep(0.01)
		if IR.value() <= 30:
			Motor_Lock.acquire()
			#Sound.speak('move bitch get out da way')
			SEEN_SOMEONE = 1
			RIGHT_MOTOR.stop(stop_action='brake')
			LEFT_MOTOR.stop(stop_action='brake')
			# IR.mode = 'US-LISTEN'
			# if IR.other_sensor_present:
			# 	print("OTHER SENSOR")
			# 	SEEN_SOMEONE = 0
			# 	IR.mode = 'US-DIST-CM'
			# 	Motor_Lock.release()
			# 	sleep(5)
			# else:
			while IR.value() <= 30:	
				sleep(1)
			Motor_Lock.release()
			SEEN_SOMEONE = 0

def checkForBoundary():

	global SEEN_WHITE
	global TURNING

	TURNING = 0

	while not BTN.any():
		
		curr_val = COLOR.value()
		sleep(0.01)
		if curr_val == 6:
			if SEEN_WHITE:
				sleep(.5)
				Motor_Lock.release()
				SEEN_WHITE = 0
			else:
				print("SEEING WHITE")
				Sound.speak('Turning Around')
				Motor_Lock.acquire()
				LEFT_MOTOR.stop(stop_action='brake')
				RIGHT_MOTOR.run_forever(speed_sp=SPEED)
				if (TURNING == 0):
					HEAD_MOTOR.run_to_rel_pos(position_sp=180, speed_sp = SPEED, stop_action='brake')
					TURNING = 1
				else:
					HEAD_MOTOR.run_to_rel_pos(position_sp=-180, speed_sp = SPEED, stop_action='brake')
				SEEN_WHITE = 1
				sleep(1)


def checkForSeeker():
	pass




def turn(degrees):

	
	LEFT_MOTOR.stop(stop_action='brake')
	RIGHT_MOTOR.stop(stop_action='brake')
	
	circle = 2*math.pi*GOALIE_WIDTH
	proportion = abs(degrees)/360
	dist = circle * proportion
	n_rots = math.ceil(dist/WHEEL_CIRC)
	print(n_rots)

	if degrees > 0:
		RIGHT_MOTOR.run_to_rel_pos(position_sp=30, speed_sp = SPEED, stop_action='brake')
		HEAD_MOTOR.run_to_rel_pos(position_sp=30, speed_sp = SPEED, stop_action='brake')
		#LEFT_MOTOR.run_to_rel_pos(position_sp=-n_rots, speed_sp = SPEED, stop_action='brake')
	else:
		LEFT_MOTOR.run_to_rel_pos(position_sp=30, speed_sp = SPEED, stop_action='brake')
		HEAD_MOTOR.run_to_rel_pos(position_sp=30, speed_sp = SPEED, stop_action='brake')
		#RIGHT_MOTOR.run_to_rel_pos(position_sp=-n_rots, speed_sp = SPEED, stop_action='brake')

	

	return 


def turnAround():

	global DIRECTION

	Head_Lock.acquire()
	HEAD_MOTOR.rotate(90)
	Motor_Lock.acquire(True)
	DIRECTION = DIRECTION * -1

	turn(185*DIRECTION)
	sleep(5)
	Motor_Lock.release()
	HEAD_MOTOR.rotateTo()

	Head_Lock.release()


def blockPlayer():
	pass

def main():

	patrol_th    	   = threading.Thread(target=patrol)
	boundary_th  	   = threading.Thread(target=checkForBoundary)
	checkForEnemies_th = threading.Thread(target=checkForEnemies)
	
	checkForEnemies_th.start()
	patrol_th.start()
	boundary_th.start()

	checkForEnemies_th.join()
	boundary_th.join()
	patrol_th.join()

SEEN_WHITE   = 0

GOALIE_WIDTH = 22.5
WHEEL_CIRC   = 11.5

START_POS    = 0.0

DIRECTION    = 1
SEES_ROBOT   = False

SPEED        = 180

BTN          = Button()

RIGHT_MOTOR  = LargeMotor('outD')
LEFT_MOTOR   = LargeMotor('outA')
HEAD_MOTOR   = LargeMotor('outC')

Motor_Lock   = threading.Lock()
Head_Lock    = threading.Lock()

COLOR        = ColorSensor()
COLOR.mode   = 'COL-COLOR'
IR 			 = UltrasonicSensor()
IR.mode      = 'US-DIST-CM'
main()



