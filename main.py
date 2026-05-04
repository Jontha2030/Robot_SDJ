#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
from speaker import Speaker
from SRF02 import distance_scan
import time
from controller import controller_sturcture
import threading
from servo import selfturning_servos, servo_init
from __init__ import SRF02_data, lock
    
    
# ---------Global breytur------------
UPPER_BOUNDS = 40 # cm, Fjarlægð sem róbót byrjar að beygja við
TURNING_SPEED = 200 # Hraði mótora í beygju
FORWARD_SPEED = 150 # Hraði mótora þegar keyrt er beint áfram
REVERSE_SPEED = 160 # Hraði mótora þegar bakkað er
AVOID_TIMES = 0.04 # Fastur tími sem róbót hefur mótora í gangi þegar hann er að forðast hluti
SWEEP_TIME = 0.1 # Tíminn sem tekur servo'a að taka eitt sveim


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
    # Bý til tvo threads þar sem að eftirfarandi tveir hlutir keyra  með while loopum
    try:
        SRF02thread = threading.Thread(target=distance_scan, daemon=True) # Einn fyrir SRF02 fjarlægðarskynjarann
        servothread = threading.Thread(target=selfturning_servos, daemon=True) # Einna fyrir servoana
        SRF02thread.start()
        servothread.start()
        time.sleep(0.8)
    
        servo_init([0,1]) # Þetta virkjar servo'a og gefur þeim upphafsstöðuna 90°, sem er miðjan á bili þeirra (0-180°)
        
        speakers() # Spila lag
        
    except Exception as InitError:
        print("Einhvað fór úrsskeiðis við virkjun: ", InitError)
    
    current_state = None # Nota þessa breytu til þess að þurfa ekki að senda boð á Motorcontroller'a aftur og aftur
    try:
        while True:
            with lock: # Lock er tengt threads
                # Hér eru thread breyturnar tengdar fjarlægðarskynjaranum en þær geyma mælda fjarlægð
                distance_v = SRF02_data["left"] 
                distance_h = SRF02_data["right"]
                
            if distance_v is None or distance_h is None: # Þetta er til þess að forrit chrash'ar ekki í fyrstu umferð, en þá skilar SFR02 forritið studnum None
                time.sleep(0.1)
                continue
            
            #print("Vinstri:",distance_v," Hægri:",distance_h) #----Debug
            # Hér kemur logic'ið til þess að forðast hluti (valdar fjarlægðir fundust með að prufa)
            if 1 < distance_v < UPPER_BOUNDS: # Athugar hvort vinstri skynjari sé innan marka 
                if current_state != "beygja":
                    #print("STOP! Beygji til vinstri") #----Debug
                    # Kalla á föllin sem keyra mótórana með Motor controllernum
                    stop()
                    time.sleep(0.01)
                    backwards(REVERSE_SPEED)
                    time.sleep(AVOID_TIMES)
                    right(TURNING_SPEED)
                    time.sleep(AVOID_TIMES)
                    current_state = "beygja"
                    
            elif 1 < distance_h < UPPER_BOUNDS: # Athugar hvort hægri skynjari sé innan marka
                if current_state != "beygja":
                    #print("STOP! Beygji til hægri") #----Debug
                    # Kalla á föllin sem keyra mótórana með Motor controllernum
                    stop()
                    time.sleep(0.01)
                    backwards(REVERSE_SPEED)
                    time.sleep(AVOID_TIMES)
                    left(TURNING_SPEED)
                    time.sleep(AVOID_TIMES)
                    current_state = "beygja"
                
            else: # Ef engin hætta er skynjuð, keyrir bíllinn bara áfram
                if current_state != "afram":
                    #print("You good, áfram!") #----Debug
                    forward(FORWARD_SPEED)
                    current_state = "afram"
                    
    # Hér er gripið errora og þegar notandi slekkur á forritinu og séð til þess að slökkt er á mótórum
    except Exception as keyrsluError:
        print("Ehv. for úrskeiðis", keyrsluError)
        stop()
        
    except KeyboardInterrupt:
        print("Notandi slökkti á forriti")
        stop()


