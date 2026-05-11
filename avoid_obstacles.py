from motor import forward, backwards, right, left, stop
from play import play_random, stop_playing
import time
import threading
from servo import selfturning_servos, servo_init
from __init__ import SRF02_data, Button_Press, lock

# ---------Global breytur------------
UPPER_BOUNDS = 40 # cm, Fjarlægð sem róbót byrjar að beygja við
TURNING_SPEED = 100 # Hraði mótora í beygju
FORWARD_SPEED = 150 # Hraði mótora þegar keyrt er beint áfram
REVERSE_SPEED = 150 # Hraði mótora þegar bakkað er
AVOID_TIMES = 0.1 # Fastur tími sem róbót hefur mótora í gangi þegar hann er að forðast hluti
SWEEP_TIME = 0.1 # Tíminn sem tekur servo'a að taka einn sveim

def avoid_obstacles():
    # Bý til tvo threads þar sem að eftirfarandi tveir hlutir keyra  með while loopum
    try:        
        stop_event = threading.Event()
        servothread = threading.Thread(target=selfturning_servos, daemon=True) # Einna fyrir servoana
        servothread.start()
        time.sleep(0.8)
    
        servo_init([0,1]) # Þetta virkjar servo'a og gefur þeim upphafsstöðuna 90°, sem er miðjan á bili þeirra (0-180°)
        
        # Spilar lag
        play_random()        

        print("AUTO-MODE active")
        
    except Exception as InitError:
        print("Einhvað fór úrsskeiðis við virkjun: ", InitError)
    
    current_state = None # Nota þessa breytu til þess að þurfa ekki að senda boð á Motorcontroller'a aftur og aftur
    try:
        while True:
            with lock: # Lock er tengt threads
                # Hér eru thread breyturnar tengdar fjarlægðarskynjaranum en þær geyma mælda fjarlægð
                distance_v = SRF02_data["left"] 
                distance_h = SRF02_data["right"]
                button_status = Button_Press["state"]
            
            if button_status:
                print("Exiting AUTO-MODE...")
                #stop_playing()
                stop_event.set()
                servothread.join(timeout=2)
                break
                
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
                    backwards(REVERSE_SPEED, REVERSE_SPEED)
                    time.sleep(AVOID_TIMES)
                    right(TURNING_SPEED)
                    #time.sleep(AVOID_TIMES)
                    current_state = "beygja"
                    
            elif 1 < distance_h < UPPER_BOUNDS: # Athugar hvort hægri skynjari sé innan marka
                if current_state != "beygja":
                    #print("STOP! Beygji til hægri") #----Debug
                    # Kalla á föllin sem keyra mótórana með Motor controllernum
                    stop()
                    time.sleep(0.01)
                    backwards(REVERSE_SPEED, REVERSE_SPEED)
                    time.sleep(AVOID_TIMES)
                    left(TURNING_SPEED)
                    #time.sleep(AVOID_TIMES)
                    current_state = "beygja"
                
            else: # Ef engin hætta er skynjuð, keyrir bíllinn bara áfram
                if current_state != "afram":
                    #print("You good, áfram!") #----Debug
                    forward(FORWARD_SPEED*0.8, FORWARD_SPEED)
                    current_state = "afram"
                    
    # Hér er gripið errora og þegar notandi slekkur á forritinu og séð til þess að slökkt er á mótórum
    except Exception as keyrsluError:
        print("Ehv. for úrskeiðis", keyrsluError)
        stop()
        
    except KeyboardInterrupt:
        print("Notandi slökkti á AUTO-MODE")
        stop()
        
    print("AUTO-MODE deactivated")
        
if __name__ == "__main__":
    avoid_obstacles()
