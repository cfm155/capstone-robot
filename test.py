# Password: maker
from ev3dev.ev3 import *
from time import sleep
m = LargeMotor('outA')
m.run_timed(time_sp=3000, speed_sp=-750)
print("set speed (speed_sp) = " + str(m.speed_sp))
sleep(1)  # it takes a moment for the motor to start moving
print("actual speed = " + str(m.speed))
sleep(4)
