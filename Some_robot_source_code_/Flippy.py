#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random


#chmod 777 *
#stay in bounds done
#see ball 
#grab ball


mRt = LargeMotor('outB')
mLt = LargeMotor('outC')
mFlip = LargeMotor('outA')

#initialize touch sensor

cl = ColorSensor()
cl.mode='RGB-RAW'

ts = TouchSensor()

colorDictionary = {
  "RED" : [54, 15, 11],
  "RED_ALT" : [71, 17, 13],
  "WHITE" : [135, 186, 131],
  "BLUE" : [10, 22, 41],
  "GRAY" : [21, 29, 24],
  "YELLOW" : [82, 78, 20],
  "YELLOW_ALT" : [121, 90, 25],
  "GREEN" : [22, 64, 22],
  None : [0, 0, 0],
  }

#Returns the key (name of the color) of the color immediately below the color sensor 
def getCurrentColor() :
  arr = [cl.value(0), cl.value(1), cl.value(2)]
  asdf = False
  if arr[0] < 18 :
  	return "BLUE"
  elif arr[0] < 33 :
  	return "GRAY"
  elif arr[0] < 90 :
  	return "RED"
  elif arr[0] > 100 :
  	return "WHITE"

#helper function
def inThree(a, b) :
  if(abs(a - b) <= 7) :
    return True
  return False

#numbers need to be calibrated to individual robots, rotates the robot 180 degrees
def rotate() :
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	print("rotating")
	mLt.run_to_rel_pos(position_sp=1060, speed_sp = 200, stop_action = "brake")
	print("Left Motor Running")
	mRt.run_to_rel_pos(position_sp=-1060, speed_sp = 200, stop_action = "brake")
	print("Right motor running")
	print("finished rotating")
	sleep(6)


def whenBlue(turnRadius, turnSpeed) :
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

def whenGray(turnRadius, turnSpeed) :
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	mRt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

def whenRed(turnRadius, turnSpeed) : 
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

def flip() :
	mRt.stop()
	mLt.stop()
	mFlip.stop()
	mFlip.run_to_rel_pos(position_sp = -80, speed_sp = 700, stop_action = "hold")
	Sound.play('cena.wav')
	print("FORWARDS")
	mRt.run_timed(time_sp = 5000, speed_sp = -1000)
	mLt.run_timed(time_sp = 5000, speed_sp = -1000)
	print("WAITING")
	mRt.wait_while('running')
	mLt.wait_while('running')
	mFlip.run_to_rel_pos(position_sp = 68, speed_sp = 100, stop_action = "brake")
	print("BACKWARDS")
	mRt.run_timed(time_sp = 5000, speed_sp = 1000)
	mLt.run_timed(time_sp = 5000, speed_sp = 1000)
	sleep(6)
	


#Start with blue on the right and gray on the left, dirFlag is 0
#Move faster, and reduce sleep times
def run() :
	turnSpeedSlow = 80
	turnSpeedFast = 120
	moveSpeed = 500
	turnRadius = 130
	inbounds = True
	hasTouched = False
	dirFlag = 0
	print("Starting")
	while inbounds and not ts.value():
		mLt.run_forever(speed_sp = -350)
		mRt.run_forever(speed_sp = -350)
		col = getCurrentColor()
		print(col)
		if col == "WHITE" :
			mLt.stop()
			mRt.stop()
			rotate()
			print("resuming movement")
			turnSpeedFast *= -1
			turnSpeedSlow *= -1
			if dirFlag == 0 :
				dirFlag = 1
			else :
				dirFlag = 0

		elif col == "BLUE" and dirFlag == 0 :
			whenBlue(turnRadius, turnSpeedFast)

		elif (col == "RED" or col=="RED_ALT") and dirFlag == 1 :
			whenRed(turnRadius, turnSpeedFast)

		elif col == "GRAY" :
			if dirFlag == 0 :
				whenGray(turnRadius, turnSpeedFast)
			else :
				whenGray(turnRadius, -turnSpeedFast)

		sleep(0.05)
	flip()	
	run()



run()