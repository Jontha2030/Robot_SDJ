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
    time.sleep(0.8)
    servo.servo_init([0,1])

    current_state = None
    try:
        while True:
            with lock:
                distance_v = SRF02_data["left"]
                distance_h = SRF02_data["right"]
                
            if distance_v is None or distance_h is None:
                time.sleep(0.1)
                continue
            
            print("Vinstri:",distance_v," Hægri:",distance_h) #----Debug
            if 0 > distance_v and distance_v < 30:
                if current_state != "beygja":
                    print("STOP! Beygji til vinstri") #----Debug
                    stop()
                    time.sleep(0.01)
                    right()
                    current_state = "beygja"
                    
            elif 0 > distance_h and distance_h < 30:
                if current_state != "beygja":
                    print("STOP! Beygji til hægri") #----Debug
                    stop()
                    time.sleep(0.01)
                    left()
                    current_state = "beygja"
                
            else:
                if current_state != "afram":
                    print("You good, áfram!")
                    forward()
                    current_state = "afram"
                    
    except Exception as e:
        print("Ehv. for úrskeiðis", e)
        stop()
        
    except KeyboardInterrupt:
        print("Forrit er hætt")
        stop()

avoid_obstacles()
