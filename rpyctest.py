#!/usr/bin/env python3
import rpyc
conn = rpyc.classic.connect('169.254.78.81') # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely
m = ev3.LargeMotor('outA')
m.run_timed(time_sp=1000, speed_sp=600)