#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time   import sleep

# Connect EV3 color and touch sensors to any sensor ports
cl1 = ColorSensor('in1')
cl4 = ColorSensor('in4') 


# Put the color sensor into COL-COLOR mode.
cl1.mode='COL-COLOR'
cl4.mode='COL-COLOR'

colors=('unknown','black','blue','green','yellow','red','white','brown')
always = True
while always:    # Stop program by pressing touch sensor button
    print("SensorA color: ", colors[cl1.value()])
    print("SensorD color: ", colors[cl4.value()])
    #Sound.speak(colors[cl.value()]).wait()
    sleep(1)
Sound.beep()