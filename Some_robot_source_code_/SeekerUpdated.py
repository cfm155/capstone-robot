#!/usr/bin/env python3
from ev3dev.ev3 import *
import threading
import math
from time import sleep

'''
Notes:
SQUIRREL_WIDTH = 25.5
Wheel circ : 11.5cm

What should we do if we see another robot??
'''

UNKNOWN = 0
BLACK = 1
BLUE = 2
GREEN = 3
YELLOW = 4
RED = 5
WHITE = 6
BROWN = 7

STAY_IN_BOUNDS = True 
CROSS_RED_BLUE = False
FOLLOW_YELLOW_GREEN = True
HEAD_SOUTH = True

MAX_OUTERCOUNT = 6
MAX_INNERCOUNT = 30
MIN_SPEED = 100
MAX_SPEED = 200
DELAY = 0.1
SLOW_TURN_SPEED = 50
FAST_TURN_SPEED = 100
TURN_DELAY = 2.5
ESCAPE_DELAY = 1.5
CRAWL_SPEED = 100
WIGGLE_FACTOR = 0.2

hit_first_color = False
FOLLOWING_LINE = False
col = UNKNOWN
prev_col = UNKNOWN

SQUIRREL_WIDTH = 25.5
SEEN_WHITE = False

GOING_HOME = False
LOOKING_FOR_BALL = False
FOLLOW_YELLOW_GREEN = True
HAS_BALL   = False
CLAW_DOWN  = False

hit_first_color = False


def turn(degrees, LEFT_MOTOR, RIGHT_MOTOR):

	Motor_Lock.acquire(True)
	LEFT_MOTOR.stop(stop_action='brake')
	RIGHT_MOTOR.stop(stop_action='brake')
	
	circle = 2*math.pi*SQUIRREL_WIDTH
	proportion = abs(degrees)/360
	dist = circle * proportion
	n_rots = math.ceiling(dist/WHEEL_CIRC)

	if degrees > 0:
		RIGHT_MOTOR.run_to_rel_pos(position_sp=n_rots, speed_sp = 120, stop_action='brake')
	else:
		LEFT_MOTOR.run_to_rel_pos(position_sp=n_rots, speed_sp = 120, stop_action='brake')

	Motor_Lock.release()
	return 


def checkForRobots():

	global GAME_OVER
	global LOOKING_FOR_BALL
	global GOING_HOME
	global HEAD_THRES
	global HEAD_US

	HEAD_US.mode = "US-DIST-CM"

	while GOING_TO_ENEMY:

		sleep(0.01)
		head_val = HEAD_US.value()
		
		if head_val <= HEAD_THRES:
			print("DANGER!!")
			Motor_Lock.acquire(True)
			# RIGHT_MOTOR.run_forever(speed_sp = SPEED)
			# LEFT_MOTOR.run_forever(speed_sp = -SPEED)
			# sleep(4)
			RIGHT_MOTOR.stop(stop_action='brake')
			LEFT_MOTOR.stop(stop_action='brake')
			sleep(3)
			Motor_Lock.release()

	while LOOKING_FOR_BALL:
		sleep(0.01)
		head_val = HEAD_US.value()
		if head_val <= HEAD_THRES:
			print("DANGER!!")
			
			
			Motor_Lock.acquire(True)
			RIGHT_MOTOR.run_forever(speed_sp = SPEED)
			LEFT_MOTOR.run_forever(speed_sp = -SPEED)
			sleep(4.5)
			RIGHT_MOTOR.stop(stop_action='brake')
			LEFT_MOTOR.stop(stop_action='brake')
			Motor_Lock.release()

	#HEAD_US.mode = 'US-LISTEN'

	while HAS_BALL:
		sleep(0.01)
		head_val = HEAD_US.value()
		if GAME_OVER:
			break
		if head_val <= HEAD_THRES:
			print("DANGER!!")
			Motor_Lock.acquire(True)
			# RIGHT_MOTOR.run_forever(speed_sp = SPEED)
			# LEFT_MOTOR.run_forever(speed_sp = -SPEED)
			# sleep(4)
			RIGHT_MOTOR.stop(stop_action='brake')
			LEFT_MOTOR.stop(stop_action='brake')
			sleep(3)
			Motor_Lock.release()
		# sleep(0.01)
		# if HEAD_US.other_sensor_present():
		# 	Motor_Lock.acquire(True)
		# 	RIGHT_MOTOR.stop(stop_action='brake')
		# 	LEFT_MOTOR.stop(stop_action='brake')
		# 	while HEAD_US.other_sensor_present():
		# 		sleep(2)
		# 	Motor_Lock.release()

def patrol(speed_sp=-200):
	#Drive back and forth
	#speed
	print("GO GO GADGET PATROL THREAD")
	while not GAME_OVER:
		print("PATROLLING")
		sleep(1)
		Motor_Lock.acquire(True)

		RIGHT_MOTOR.run_forever(speed_sp = speed_sp)
		LEFT_MOTOR.run_forever(speed_sp = speed_sp)

		Motor_Lock.release()
	Motor_Lock.acquire(True)
	print("GAME OVER")
	RIGHT_MOTOR.stop(stop_action='brake')
	LEFT_MOTOR.stop(stop_action = 'brake')


def checkDirection(LEFT_MOTOR, RIGHT_MOTOR, color, going_home=False):
	# 2 is blue and 5 is red
	Motor_Lock.acquire(True)
	Color_Lock.acquire(True)
	code = getCurrentColor()
	i = 0
	
	if going_home:
		#blue then red
		first = 2
		second = 5
	else:
		#red then blue
		first = 5
		second = 2

	if code != second and code != second:
		#Not red or blue
		Motor_Lock.release()
		return

	else:
		if code == second:
			#We first see the color that's supposed to come second
			#Wrong way
			LEFT_MOTOR.stop(stop_action='brake')
			RIGHT_MOTOR.stop(stop_action='brake')
			Motor_Lock.release()
			turn(180, LEFT_MOTOR=LEFT_MOTOR, RIGHT_MOTOR=RIGHT_MOTOR)

		elif code == first:
			#We see the correct color first
			#Right Way
			LEFT_MOTOR.stop(stop_action='brake')
			RIGHT_MOTOR.stop(stop_action='brake')

			while i < 5:
				#Check for second color
				LEFT_MOTOR.run_forever(speed_sp=100)
				RIGHT_MOTOR.run_forever(speed_sp=100)
				code = getCurrentColor()
				if code == second:
					return
				sleep(.5)
				i+=1

			#We didn't see the second color. Turn around?
			Motor_Lock.release()
			turn(180, LEFT_MOTOR=LEFT_MOTOR, RIGHT_MOTOR=RIGHT_MOTOR)

	color.mode='COL-REFLECT'
	Color_Lock.release()
	return

def checkForBall():

	print("GO GO GADGET BALL THREAD")

	while not GAME_OVER:
		if BALL_IR.value() <= 8 and not HAS_BALL and not GOING_TO_ENEMY:
			print("BALL BALL BALL BALL!!")
			captureBall()
		sleep(.5)


#Returns the key (name of the color) of the color immediately below the color sensor 

def getCurrentColor() :

  curr = COLOR.value()
  arr = [COLOR.value(0), COLOR.value(1), COLOR.value(2)]

  asdf = False

  for key, val in colorDictionary.items() : 

    if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :

      return key



#helper function

def inThree(a, b) :

  if(abs(a - b) <= 3) :

    return True

  return False



def captureBall():

	global HAS_BALL
	global CLAW_DOWN
	global GOING_HOME
	global LOOKING_FOR_BALL

	# Move the claw 90 degrees, hopefully in the right direction
	CLAW_MOTOR.run_to_rel_pos(position_sp=90, speed_sp=150, stop_action='brake')

	HAS_BALL   = True
	CLAW_DOWN  = True
	GOING_HOME = True
	LOOKING_FOR_BALL = False

	return

def checkForAllBoundary():

	print("GO GO GADGET BOUNDARY THREAD")
	global SEEN_RED
	global GAME_OVER
	global COLOR
	global SEEN_WHITE
	global GOING_TO_ENEMY
	global LOOKING_FOR_BALL

	#COLOR.mode = 'COL-COLOR'

	while LOOKING_FOR_BALL:
		#When we have the ball we want to ignore all this and just go home
		Color_Lock.acquire(True)
		sleep(0.01)
		curr_val = getCurrentColor()
		Color_Lock.release()
		
			
		if curr_val == RED:
			if GOING_TO_ENEMY:
				if SEEN_RED:
					SEEN_RED = 0
					GOING_TO_ENEMY = False
					print("WE MADE IT")
					# We made it into enemy territory
				else:
					print("HALF WAY THERE")
					SEEN_RED = 1
				sleep(3)
			else:
				# if SEEN_RED:
				# 	sleep()
				# 	Motor_Lock.release()
				# 	SEEN_RED = 0
					
				
				print("SEEING RED")
				Motor_Lock.acquire()
				RIGHT_MOTOR.stop(stop_action='brake')
				LEFT_MOTOR.run_forever(speed_sp=SPEED)
				SEEN_RED = 1
				sleep(8)
				print("SHOULD STOP TURNING")
				Motor_Lock.release()
		
		

		elif curr_val == WHITE:
			# If we hit white, we are hitting the boundary
			if SEEN_WHITE:
				sleep(2.5)
				Motor_Lock.release()
				SEEN_WHITE = 0
				print("SHOULD STOP TURNING")
				
			else:
				print("SEEING WHITE")
				Motor_Lock.acquire()
				LEFT_MOTOR.stop(stop_action='brake')
				RIGHT_MOTOR.run_forever(speed_sp=SPEED)
				SEEN_WHITE = 1
				sleep(2)

	print("NOT LOOKING FOR BALL")
	while not GAME_OVER:
		#print("NOT LOOKING FOR BALL")
		curr_val = getCurrentColor()
		sleep(0.01)
		if curr_val == RED:
			print("NOT LOOKING FOR BALL--RED")
			if SEEN_RED:
				sleep(7)
				SEEN_RED = 0
				# GAME_OVER = True
				# print("GAME OVERRRR")
				# return
			else:
				print("HALF WAY HOME!!")
				SEEN_RED = 1
				sleep(4)



# def checkForRBBoundary():

# 	COLOR.mode = 'COL-COLOR'

# 	global SEEN_RED
# 	global GAME_OVER
# 	global COLOR


# 	while LOOKING_FOR_BALL:
# 		#When we have the ball we want to ignore all this and just go home
# 		Color_Lock.acquire(True)
# 		sleep(0.01)
# 		curr_val = getCurrentColor()
# 		Color_Lock.release()
# 		if curr_val == RED:
# 			if SEEN_RED:
# 				sleep(1)
# 				Motor_Lock.release()
# 				SEEN_RED = 0
				
# 			else:
# 				print("SEEING RED")
# 				Motor_Lock.acquire()
# 				RIGHT_MOTOR.stop(stop_action='brake')
# 				LEFT_MOTOR.run_forever(speed_sp=SPEED)
# 				SEEN_RED = 1
# 				sleep(2)
		
# 		elif curr_val == BLUE:
# 			#If we hit blue first, then we're going to enemy territory
# 			sleep(4)



# 	while not GAME_OVER:

# 		curr_val = getCurrentColor()
# 		sleep(0.01)
# 		if curr_val == RED:
# 			if SEEN_RED:
# 				sleep(4)
# 				SEEN_RED = 0
# 				GAME_OVER = True
# 				return
# 			else:
# 				SEEN_RED = 1



# def checkForWBoundary():

# 	global SEEN_WHITE
# 	global GAME_OVER
# 	global COLOR

# 	while not GAME_OVER:
# 		Color_Lock.acquire(True)
# 		sleep(0.01)
# 		curr_val = getCurrentColor()
# 		Color_Lock.release()
		
# 		if curr_val == WHITE:
# 			if SEEN_WHITE:
# 				sleep(4)
# 				Motor_Lock.release()
# 				SEEN_WHITE = 0
# 				print("SHOULD STOP TURNING")
				
# 			else:
# 				print("SEEING WHITE")
# 				Motor_Lock.acquire()
# 				LEFT_MOTOR.stop(stop_action='brake')
# 				RIGHT_MOTOR.run_forever(speed_sp=SPEED)
# 				SEEN_WHITE = 1
# 				sleep(2)

def followYG():

	UNKNOWN = 0
	BLACK = 1
	BLUE = 2
	GREEN = 3
	YELLOW = 4
	RED = 5
	WHITE = 6
	BROWN = 7


	STAY_IN_BOUNDS = True 
	CROSS_RED_BLUE = False
	FOLLOW_YELLOW_GREEN = True
	HEAD_SOUTH = True

	GAME_OVER  = False

	MAX_OUTERCOUNT = 6
	MAX_INNERCOUNT = 30
	MIN_SPEED = 100
	MAX_SPEED = 200
	DELAY = 0.1
	SLOW_TURN_SPEED = 50
	FAST_TURN_SPEED = 100
	TURN_DELAY = 2.5
	ESCAPE_DELAY = 1.5
	CRAWL_SPEED = 100
	WIGGLE_FACTOR = 0.2

	hit_first_color = False
	FOLLOWING_LINE = False
	col = UNKNOWN
	prev_col = UNKNOWN

	SQUIRREL_WIDTH = 25.5
	SEEN_WHITE = False

	GOING_HOME = False
	LOOKING_FOR_BALL = True
	FOLLOW_YELLOW_GREEN = True
	HAS_BALL   = False
	CLAW_DOWN  = False

	hit_first_color = False

	while True:
		  # If looking for yellow/green strip to follow 
	    if (FOLLOW_YELLOW_GREEN and not(FOLLOWING_LINE)):
	      if (not(hit_first_color) and (col == GREEN or col == YELLOW)):
	        # Hit first of two colors 
	        hit_first_color = True
	        mRt.run_forever(speed_sp= -SLOW_TURN_SPEED)
	        mLt.run_forever(speed_sp= -SLOW_TURN_SPEED)
	      elif hit_first_color:
	        if (col != YELLOW and col != GREEN):
	          col = prev_col   # ignore bad color reading? 
	        else:
	          if ((prev_col == YELLOW and col == GREEN)
	          or (prev_col == GREEN and col == YELLOW)):
	          # Hit second of two colors 
	            prev_col = col
	            if ((col == GREEN and HEAD_SOUTH)
	            or (col == YELLOW and not(HEAD_SOUTH))):
	              sign = -1
	            else:
	              sign = 1
	            mRt.run_forever(speed_sp=  sign * SLOW_TURN_SPEED)
	            mLt.run_forever(speed_sp= -sign * SLOW_TURN_SPEED)
	            while prev_col == col:
	              sleep(DELAY)
	              col = cl.value()
	              if col == BROWN:
	                col = YELLOW
	              if (col != GREEN and col != YELLOW):
	                col = prev_col
	              print(colors[col])
	            FOLLOWING_LINE = True  # now on yellow/green and following
	            hit_first_color = False

	    # If on and following yellow/green strip
	    if (FOLLOW_YELLOW_GREEN and FOLLOWING_LINE):
	      if (col != GREEN and col != YELLOW):
	        col = prev_col
	      if ((col == YELLOW and GOING_HOME) or
	      (col == GREEN and not(GOING_HOME))):
	        mRt.run_forever(speed_sp= -CRAWL_SPEED*WIGGLE_FACTOR)
	        mLt.run_forever(speed_sp= -CRAWL_SPEED)
	      if ((col == GREEN and GOING_HOME) or
	      (col == YELLOW and not(GOING_HOME))):
	        mRt.run_forever(speed_sp= -CRAWL_SPEED)
	        mLt.run_forever(speed_sp= -CRAWL_SPEED*WIGGLE_FACTOR)

#########



colorDictionary = {

  "RED" : [70, 11, 18],

  "WHITE" : [119, 94, 179],

  "BLUE" : [14, 16, 61],

  "GRAY" : [28, 21, 34],

  "YELLOW" : [84, 48, 28],

  "GREEN" : [22, 37, 30],

  None : [0, 0, 0],

  }

########


UNKNOWN = "UNKNOWN"
BLACK = "BLACK"
BLUE = "BLUE"
GREEN = "GREEN"
YELLOW = "YELLOW"
RED = "RED"
WHITE = "WHITE"
BROWN = "BROWN"

SPEED        = -180

STAY_IN_BOUNDS = True 
CROSS_RED_BLUE = False
FOLLOW_YELLOW_GREEN = True
HEAD_SOUTH = True

MAX_OUTERCOUNT = 6
MAX_INNERCOUNT = 30
MIN_SPEED = 100
MAX_SPEED = 200
DELAY = 0.1
SLOW_TURN_SPEED = 50
FAST_TURN_SPEED = 100
TURN_DELAY = 2.5
ESCAPE_DELAY = 1.5
CRAWL_SPEED = 100
WIGGLE_FACTOR = 0.2


hit_first_color = False
FOLLOWING_LINE = False
col = UNKNOWN
prev_col = UNKNOWN


SQUIRREL_WIDTH = 25.5
SEEN_WHITE = False
SEEN_RED   = False
SEEN_BLUE  = False

GAME_OVER = False
GOING_HOME = False
GOING_TO_ENEMY = True
LOOKING_FOR_BALL = True
HEAD_THRES = 20


HAS_BALL   = False
CLAW_DOWN  = False

hit_first_color = False

RIGHT_MOTOR = LargeMotor('outA')
LEFT_MOTOR  = LargeMotor('outB')
CLAW_MOTOR  = LargeMotor('outD')

COLOR 		= ColorSensor()
COLOR.mode = 'RGB-RAW'

Motor_Lock = threading.Lock()
Color_Lock = threading.Lock()
Head_Lock  = threading.Lock()



HEAD_US    		  = UltrasonicSensor()
HEAD_US.mode      = 'US-DIST-CM'

BALL_IR    		  = InfraredSensor()
BALL_IR.mode      = 'IR-PROX'

#CLAW_MOTOR.stop(stop_action='brake')
ball_th           = threading.Thread(target=checkForBall)
patrol_th         = threading.Thread(target=patrol)

defense_th 		  = threading.Thread(target=checkForRobots)
boundary_th       = threading.Thread(target=checkForAllBoundary)

startpos = 0

print("everything should be working")


ball_th.start()

boundary_th.start()
patrol_th.start()
defense_th.start()


ball_th.join()
defense_th.join()
boundary_th.join()
patrol_th.join()