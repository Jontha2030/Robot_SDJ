from evdev import InputDevice, ecodes
from motor import forward, backwards, right, left, stop
from play import play_random, stop_playing
from SRF02 import distance_scan
from __init__ import Button_Press
import threading
import time
import avoid_obstacles

speed = 200
def initialize_components():
    SRF02Thread = threading.Thread(target=distance_scan, daemon=True) # Búum til þráð fyrir fjarlægðarskynjarana sem keyrir alltaf
    # þar sem það var vesen að slökkva og kveikja á honum
    SRF02Thread.start()

#Fall fyrir controller
def controller_sturcture():
    try:
        dev = InputDevice("/dev/input/event4")

        #Skillgreini takka
        BTN_X = 304
        BTN_CIRCLE = 305
        BTN_TRIANGLE = 307
        BTN_SQUARE = 308

        BTN_L1 = 310
        BTN_R1 = 311
        BTN_L2 = 312
        BTN_R2 = 313
        BTN_R3 = 318

        print("Controller ready")


        #Ef ýtt er á taka þá gerist eitthvað
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                if event.code == BTN_X:
                    backwards(speed)
                elif event.code == BTN_CIRCLE:
                    right(speed)
                elif event.code == BTN_TRIANGLE:
                    forward(speed)
                elif event.code == BTN_SQUARE:
                    left(speed)
                elif event.code == BTN_R1:
                    stop()
                elif event.code == BTN_R2:
                    print("R2 pressed")
                elif event.code == BTN_L1:
                    Button_Press["state"] = False
                    print("L1 pressed")
                    print("Entering AUTO-MODE...")
                    automodeThread = threading.Thread(target=avoid_obstacles.avoid_obstacles, daemon=True)
                    automodeThread.start()
                elif event.code == BTN_L2:
                    print("L2 pressed")
                    Button_Press["state"] = True
                    stop()
                    automodeThread.join(timeout=2)
                    
                elif event.code == BTN_R3:
                    print("R3 pressed")


            #Þetta er fyrir D-pad
            elif event.type == ecodes.EV_ABS:
                if event.code == ecodes.ABS_HAT0Y:
                    if event.value == -1:
                        print("D-pad up")
                    elif event.value == 1:
                        print("D-pad down")

                elif event.code == ecodes.ABS_HAT0X:
                    if event.value == -1:
                        stop_playing()
                        print("D-pad left")
                    elif event.value == 1:
                        play_random()
                        print("D-pad right")
                        
    except KeyboardInterrupt:
        print("Notandi slökkti á forriti")
        stop()
        Button_Press["state"] = False

                        

if __name__ == "__main__":
    initialize_components()
    controller_sturcture()
