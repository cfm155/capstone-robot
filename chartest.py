#!/usr/bin/env python3
 
# adapted from https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_keyboard.py
from ev3dev.ev3 import *
from time import sleep
import sys, termios, tty, os, time
import fcntl
 
mA = LargeMotor('outA')
mD = LargeMotor('outD')

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 
button_delay = 0.2

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
 
while True:
    sleep(1)
    char = getch()
    sleep(1)
 
    if (char == "p"):
        print("Stop!")
        exit(0)
 
    elif (not char):
        print("No char")
    elif (char == "a"):
        print("Left pressed")
        mA.run_timed(time_sp=1000, speed_sp=750)
        time.sleep(button_delay)
 
    elif (char == "d"):
        print("Right pressed")
        mD.run_timed(time_sp=1000, speed_sp=750)
        time.sleep(button_delay)
 
    elif (char == "w"):
        print("Up pressed")
        mA.run_timed(time_sp=1000, speed_sp=750)
        mD.run_timed(time_sp=1000, speed_sp=750)
        time.sleep(button_delay)
 
    elif (char == "s"):
        print("Down pressed")
        mA.run_timed(time_sp=1000, speed_sp=-750)
        mD.run_timed(time_sp=1000, speed_sp=-750)
        time.sleep(button_delay)
 
    elif (char == "1"):
        print("Number 1 pressed")
        time.sleep(button_delay)