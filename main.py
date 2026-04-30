#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
import time

forward()
time.sleep(5)
right()
time.sleep(2)
backwards()
time.sleep(3)
stop()
