#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
mA = LargeMotor('outA')
mD = LargeMotor('outD')
# Connect infrared and touch sensors to any sensor ports
ir = InfraredSensor() 

# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'
mA.run_forever(speed_sp=300)
mD.run_forever(speed_sp=300)

while not ir.value() < 50:    # Stop program by pressing touch sensor button
    # Infrared sensor in proximity mode will measure distance to the closest
    # object in front of it.
    distance = ir.value()

    if distance < 75:
        Leds.set_color(Leds.LEFT, Leds.RED)
    else:
        Leds.set_color(Leds.LEFT, Leds.GREEN)
mA.stop(stop_action= "brake")
mD.stop(stop_action= "brake")
Sound.beep()       
Leds.set_color(Leds.LEFT, Leds.GREEN)  
#make sure left led is green before exiting