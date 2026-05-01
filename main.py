#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
from speaker import Speaker
from SRF02 import distance_scan
import time
import threading
import servo
from __init__ import SRF02_data, lock
    

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

def avoid_obstacles():
    t = threading.Thread(target=distance_scan, daemon=True)
    t.start()
    
    while True:
        with lock:
            distance_v = SRF02_data["left"]
            distance_h = SRF02_data["right"]
            
        print("Vinstri:",distance_v," Hægri:",distance_h) #----Debug
        if distance_v > 0 and distance_v < 30 or distance_h > 0 and distance_h < 30:
            print("STOP! Beygji til hægri") #----Debug
            stop()
            right()
        else:
            print("You good, áfram!")
            forward()