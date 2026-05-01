#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
from speaker import Speaker
import time
from controller import controller_sturcture


def call_controller():
    controller_sturcture()


def keyra_bil():
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
def speakers():
    # Frumstilla speaker
    speaker = Speaker()

    # Þegar bíllinn fer í gang — spila lag
    print("Bíllinn fer í gang!")
    speaker.play()

call_controller()