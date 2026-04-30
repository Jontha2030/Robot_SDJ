#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
import time


while True:

    tala = input()

    if tala == 'w':
        forward()

    elif tala == 's':
        backwards()

    elif tala == 'a':
        left()

    elif tala == 'd':
        right()

    elif tala == ' ':
        stop()

    elif tala == 'q':
        stop()
        break