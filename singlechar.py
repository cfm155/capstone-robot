#!/usr/bin/env python3
# file: 'readchar.py'
"""
Implementation of a way to get a single character of input
without waiting for the user to hit <Enter>.
(OS is Linux, Ubuntu 14.04)
"""

import tty, sys, termios, subprocess, os

class ReadChar():
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

def test():
    while True:
        ifile = open("char.txt",'r')
        char = ifile.read()
        ifile.close()
        if not char:
            char = 'c'
        #with ReadChar() as rc:
        #    char = rc
        if ord(char) <= 32:
            print("You entered character with ordinal {}."\
                        .format(ord(char)))
        else:
            print("You entered character '{}'."\
                        .format(char))
        if char in "^C^D":
            sys.exit()

if __name__ == "__main__":
    test()