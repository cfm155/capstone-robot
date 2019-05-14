#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import os

# set color values
UNKNOWN = 0
BLACK = 1
BLUE = 2
GREEN = 3
YELLOW = 4
RED = 5
WHITE = 6
BROWN = 7

# initialize lane and direction
LANE = 'l'
CROSS_RED_BLUE = False
HEAD_NORTH = True

# set values for inner and outer counts of loop (these values last about 1 full lap on our track)
MAX_OUTERCOUNT = 10
MAX_INNERCOUNT = 30

# set speed values and delay values (to allow for turning)
SPEED = 100
DELAY = 0.1
TURN_SPEED = 100
TURN_DELAY = 3
STRAIGHT_DELAY = 1
LANE_CHANGE_DELAY = 2.5
WIGGLE_SPEED = 150
WIGGLE_FACTOR = 0.2

# initialize robot to not following line, with colors unknown
hit_first_color = False
following_line = False
color = UNKNOWN
prev_color = UNKNOWN

# assign motor and colorsensor variables
motorFL = LargeMotor('outA')
motorBL = LargeMotor('outB')
motorBR = LargeMotor('outC')
motorFR = LargeMotor('outD')
colSens = ColorSensor('in4')
colSens.mode = 'COL-COLOR'
colors = ('unknown','black','blue','green','yellow','red','white','brown')
color = 0

# create a getColor function to allow for retrieving of color as well as printing of color to watch for errors
def getColor():
    global color
    color = colSens.value()
    print(colors[color])
# start the robot moving forward
motorFR.run_forever(speed_sp= SPEED)
motorBR.run_forever(speed_sp= -(SPEED))
motorBL.run_forever(speed_sp= -(SPEED))
motorFL.run_forever(speed_sp= SPEED)

# start the main logic of robot
for outercount in range(MAX_OUTERCOUNT):
  for innercount in range(MAX_INNERCOUNT):
    # make sure to sleep so that the loop is not running too quickly
    sleep(DELAY)

    # check if the object.txt file exists, meaning the camera has detected an object
    exists = os.path.isfile('object.txt')
    if exists and following_line:
      # if there is an object and the robot is following a line, remove the object.txt file and change lanes
      print("object detected")
      Sound.beep()
      os.system("rm object.txt")
      # no longer following a line since the robot is changing lanes
      following_line = False
      if LANE == 'r':
        # if in the right lane, turn to the left, move forward, then turn right, changing the lane to the left lane
        motorFR.run_forever(speed_sp=SPEED + TURN_SPEED)
        motorBR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        sleep(TURN_DELAY)
        motorFR.run_forever(speed_sp=SPEED)
        motorBR.run_forever(speed_sp=-(SPEED))
        motorBL.run_forever(speed_sp=-(SPEED))
        motorFL.run_forever(speed_sp=SPEED)
        sleep(LANE_CHANGE_DELAY)
        motorFR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBR.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        sleep(TURN_DELAY/2)
        LANE = 'l'
      else:
        # if in the left lane, turn to the right, move forward, then turn left, changing the lane to the right lane
        motorFR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBR.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        sleep(TURN_DELAY)
        motorFR.run_forever(speed_sp=SPEED)
        motorBR.run_forever(speed_sp=-(SPEED))
        motorBL.run_forever(speed_sp=-(SPEED))
        motorFL.run_forever(speed_sp=SPEED)
        sleep(LANE_CHANGE_DELAY)
        motorFR.run_forever(speed_sp=SPEED + TURN_SPEED)
        motorBR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        sleep(TURN_DELAY/2)
        LANE = 'r'

    # if an object exists but are not following a line, remove the object since it could have detected an object while
    # turning
    elif exists:
        os.system("rm object.txt")

    # save last color and get new color
    prev_color = color
    getColor()

    # Turn around if see black border
    if color == BLACK:
      # no longer following line, now heading the opposite direction
      following_line = False
      if HEAD_NORTH == True:
        HEAD_NORTH = False
      else:
        HEAD_NORTH = True

      # if in the right lane, turn around to the left
      if LANE == 'r':
        # back up a bit first to give turning room
        motorFR.run_forever(speed_sp=-SPEED)
        motorBR.run_forever(speed_sp=SPEED)
        motorBL.run_forever(speed_sp=SPEED)
        motorFL.run_forever(speed_sp=-SPEED)
        sleep(STRAIGHT_DELAY)
        # turn left about 90 degrees
        motorFR.run_forever(speed_sp=SPEED + TURN_SPEED)
        motorBR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        sleep(TURN_DELAY)
        # go forward close to the next line
        motorFR.run_forever(speed_sp=SPEED)
        motorBR.run_forever(speed_sp=-SPEED)
        motorBL.run_forever(speed_sp=-SPEED)
        motorFL.run_forever(speed_sp=SPEED)
        sleep(STRAIGHT_DELAY)
        # turn left again
        motorFR.run_forever(speed_sp=SPEED + TURN_SPEED)
        motorBR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        sleep(TURN_DELAY - 1)

      # if in the left lane, turn around to the right
      else:
        # back up a bit first to give turning room
        motorFR.run_forever(speed_sp=-SPEED)
        motorBR.run_forever(speed_sp=SPEED)
        motorBL.run_forever(speed_sp=SPEED)
        motorFL.run_forever(speed_sp=-SPEED)
        sleep(STRAIGHT_DELAY)
        # turn right about 90 degrees
        motorFR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBR.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        sleep(TURN_DELAY)
        # go forward close to the next line
        motorFR.run_forever(speed_sp=SPEED)
        motorBR.run_forever(speed_sp=-SPEED)
        motorBL.run_forever(speed_sp=-SPEED)
        motorFL.run_forever(speed_sp=SPEED)
        sleep(STRAIGHT_DELAY)
        # turn right again
        motorFR.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorBR.run_forever(speed_sp=(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp=-(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp=(SPEED + TURN_SPEED))
        sleep(TURN_DELAY - 1)

    # Looking for blue/red lane to follow
    if not following_line:
      if not hit_first_color and (color == BLUE or color == RED):
        # Hit the first color, continue forward until next color
        hit_first_color = True
        motorFR.run_forever(speed_sp= SPEED + TURN_SPEED)
        motorBR.run_forever(speed_sp= -(SPEED + TURN_SPEED))
        motorBL.run_forever(speed_sp= -(SPEED + TURN_SPEED))
        motorFL.run_forever(speed_sp= SPEED + TURN_SPEED)
      elif hit_first_color:
        if color != BLUE and color != RED:
          # ignore bad color reading
          color = prev_color
        else:
          if (prev_color == BLUE and color == RED) or (prev_color == RED and color == BLUE):
            # Hit second color, get direction to know which way to turn towards
            prev_color = color
            if (color == RED and HEAD_NORTH) or (color == BLUE and not HEAD_NORTH):
              direction = -1
            else:
              direction = 1
            # turn towards other color line
            motorFR.run_forever(speed_sp=SPEED - direction * TURN_SPEED)
            motorBR.run_forever(speed_sp=-SPEED + direction * TURN_SPEED)
            motorBL.run_forever(speed_sp=-SPEED - direction * TURN_SPEED)
            motorFL.run_forever(speed_sp=SPEED + direction * TURN_SPEED)
            while prev_color == color:
              sleep(DELAY)
              getColor()
              if color != RED and color != BLUE:
                color = prev_color
            # now following the line
            following_line = True
            hit_first_color = False
      else:
        # if no interesting color yet, continue forward
        motorFR.run_forever(speed_sp=SPEED)
        motorBR.run_forever(speed_sp=-(SPEED))
        motorBL.run_forever(speed_sp=-(SPEED))
        motorFL.run_forever(speed_sp=SPEED)


    # If on and following the line
    if following_line:
      if color != RED and color != BLUE:
        # ignore bad color reading
        color = prev_color
      # wiggle the appropriate direction depending which direction robot is going and what color it senses
      if (color == BLUE and HEAD_NORTH) or (color == RED and not HEAD_NORTH):
        motorFR.run_forever(speed_sp= WIGGLE_SPEED*WIGGLE_FACTOR)
        motorBR.run_forever(speed_sp= -WIGGLE_SPEED*WIGGLE_FACTOR)
        motorBL.run_forever(speed_sp= -WIGGLE_SPEED)
        motorFL.run_forever(speed_sp= WIGGLE_SPEED)
      if (color == RED and HEAD_NORTH) or (color == BLUE and not HEAD_NORTH):
        motorFR.run_forever(speed_sp= WIGGLE_SPEED)
        motorBR.run_forever(speed_sp= -WIGGLE_SPEED)
        motorBL.run_forever(speed_sp= -WIGGLE_SPEED*WIGGLE_FACTOR)
        motorFL.run_forever(speed_sp= WIGGLE_SPEED*WIGGLE_FACTOR)

# stop motors at the end
sleep(DELAY)
motorFR.stop(stop_action="hold")
motorBR.stop(stop_action="hold")
motorBL.stop(stop_action="hold")
motorFL.stop(stop_action="hold")
