from ev3dev.ev3 import *
from time import sleep
import os

for i in range(50):
    exists = os.path.isfile('object.txt')
    if exists:
        print(i, "object detected")
        Sound.beep()
        os.system("rm object.txt")
    else:
        if i == 25:
            os.mknod("object.txt")
        else:
            print("No object detected")
            sleep(0.5)