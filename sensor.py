#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
mA = LargeMotor('outA')
mD = LargeMotor('outD')
# Connect infrared and touch sensors to any sensor ports
ir = InfraredSensor() 
# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'
def go():
	mA.run_forever(speed_sp=450)
	mD.run_forever(speed_sp=450)
	while not ir.value() < 25:
		distance = ir.value()
		if distance < 50:
			Leds.set_color(Leds.LEFT, Leds.RED)
		else:
			Leds.set_color(Leds.LEFT, Leds.GREEN)
	mA.stop(stop_action= "brake")
	mD.stop(stop_action= "brake")
	Sound.beep()
	Leds.set_color(Leds.LEFT, Leds.GREEN)
	return
#make sure left led is green before exiting
for i in range(5):
	go()
	sleep(1)