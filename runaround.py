#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random

UNKNOWN = 0
BLACK = 1
BLUE = 2
RED = 3
BLUE = 4
RED = 5
WHITE = 6
BROWN = 7

STAY_IN_BOUNDS = True 
CROSS_RED_BLUE = False
FOLLOW_BLUE_RED = True
HEAD_SOUTH = True

MAX_OUTERCOUNT = 10
MAX_INNERCOUNT = 30
MIN_SPEED = 100
MAX_SPEED = 500
DELAY = 0.1
SLOW_TURN_SPEED = 50
FAST_TURN_SPEED = 100
TURN_DELAY = 2.5
ESCAPE_DELAY = 1.5
WIGGLE_SPEED = 100
WIGGLE_FACTOR = 0.2

hit_first_color = False
following_line = False
color = UNKNOWN
prev_color = UNKNOWN

motorFL = LargeMotor('outA')
motorBL = LargeMotor('outB')
motorBR = LargeMotor('outC')
motorFR = LargeMotor('outD')
colSens = ColorSensor()
colSens.mode='COL-COLOR'
colors=('unknown','black','blue','RED','BLUE','red','white','brown')
color = 0

def getColor(): 
    global color 
    color = colSens.value()
    if color == BLACK:  # BLUE sometimes appears to be brown 
      color = BLUE
    print(colors[color])

for outercount in range(MAX_OUTERCOUNT):
  for innercount in range(MAX_INNERCOUNT):
    sleep(DELAY)
    prev_color = color
    getColor()

    # If looking for BLUE/RED stripe to follow 
    if (FOLLOW_BLUE_RED and not(following_line)):
      if (not(hit_first_color) 
      and (color == BLUE or color == RED)):
        # Hit first of two colors 
        hit_first_color = True
        motorFR.run_forever(speed_sp= MIN_SPEED + SLOW_TURN_SPEED)
        motorBR.run_forever(speed_sp= -(MIN_SPEED + SLOW_TURN_SPEED))
        motorBL.run_forever(speed_sp= -(MIN_SPEED + SLOW_TURN_SPEED))
        motorFL.run_forever(speed_sp= MIN_SPEED + SLOW_TURN_SPEED)
      elif hit_first_color:
        if (color != BLUE and color != RED):
          color = prev_color   # ignore bad color reading? 
        else:
          if ((prev_color == BLUE and color == RED)
          or (prev_color == RED and color == BLUE)):
          # Hit second of two colors 
            prev_color = color
            if ((color == RED and HEAD_SOUTH)
            or (color == BLUE and not(HEAD_SOUTH))):
              sign = -1
            else:
              sign = 1
            motorFR.run_forever(speed_sp=  MIN_SPEED - sign * SLOW_TURN_SPEED)
            motorBR.run_forever(speed_sp=  -MIN_SPEED + sign * SLOW_TURN_SPEED)
            motorBL.run_forever(speed_sp=  -MIN_SPEED - sign * SLOW_TURN_SPEED)
            motorFL.run_forever(speed_sp=  MIN_SPEED + sign * SLOW_TURN_SPEED)
            while prev_color == color:
              sleep(DELAY)
              getColor()
              if (color != RED and color != BLUE):
                color = prev_color
            following_line = True  # now on stripe and following
            hit_first_color = False

    # If on and following BLUE/RED stripe
    if (FOLLOW_BLUE_RED and following_line):
      if (color != RED and color != BLUE):
        color = prev_color
      if ((color == BLUE and HEAD_SOUTH) or
      (color == RED and not(HEAD_SOUTH))):
        motorFR.run_forever(speed_sp= WIGGLE_SPEED*WIGGLE_FACTOR)
        motorBR.run_forever(speed_sp= -WIGGLE_SPEED*WIGGLE_FACTOR)
        motorBL.run_forever(speed_sp= -WIGGLE_SPEED)
        motorFL.run_forever(speed_sp= WIGGLE_SPEED)
      if ((color == RED and HEAD_SOUTH) or
      (color == BLUE and not(HEAD_SOUTH))):
        motorFR.run_forever(speed_sp= WIGGLE_SPEED)
        motorBR.run_forever(speed_sp= -WIGGLE_SPEED)
        motorBL.run_forever(speed_sp= -WIGGLE_SPEED*WIGGLE_FACTOR)
        motorFL.run_forever(speed_sp= WIGGLE_SPEED*WIGGLE_FACTOR)

    # Take evasive action when hitting boundary?
    #while (STAY_IN_BOUNDS and (color == WHITE or
    #(not(CROSS_RED_BLUE) and (color == RED or color == BLUE)))):
    #  motorFR.run_forever(speed_sp=  FAST_TURN_SPEED)
    #  motorBR.run_forever(speed_sp=  FAST_TURN_SPEED)
    #  motorBL.run_forever(speed_sp= -FAST_TURN_SPEED)
    #  motorFL.run_forever(speed_sp= -FAST_TURN_SPEED)
    #  sleep(TURN_DELAY)
    #  motorR.run_forever(speed_sp= -MIN_SPEED)
    #  motorL.run_forever(speed_sp= -MIN_SPEED)
    #  sleep(ESCAPE_DELAY)
    #  getColor()
    #prev_color = color

    # Change direction once in a while (literally - outer loop)
    #if (innercount == 0 and not(following_line)):
    #  leftSpeed  = - random.randint(MIN_SPEED, MAX_SPEED)
    #  rightSpeed = - random.randint(MIN_SPEED, MAX_SPEED)
    #  motorR.run_forever(speed_sp= leftSpeed)
    #  motorL.run_forever(speed_sp= rightSpeed)
    #  lineup_counter = 0

# All done
sleep(DELAY)
motorFR.stop(stop_action="hold")
motorBR.stop(stop_action="hold")
motorBL.stop(stop_action="hold")
motorFL.stop(stop_action="hold")
sleep(DELAY)
