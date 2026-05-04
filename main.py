from evdev import InputDevice, ecodes
from motor import send_motors, forward, backwards, right, left, stop
from play import play_random, get_songs, start_playing, stop_playing
from avoid_obstacles import avoid_obstacles

speed = 200
#Fall fyrir controller
def controller_sturcture():
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
                avoid_obstacles() 
                print("L1 pressed")
            elif event.code == BTN_L2:
                print("L2 pressed")
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


controller_sturcture()


