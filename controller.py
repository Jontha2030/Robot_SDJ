from evdev import InputDevice, ecodes

dev = InputDevice("/dev/input/event4")

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

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY and event.value == 1:
        if event.code == BTN_X:
            print("X pressed")
        elif event.code == BTN_CIRCLE:
            print("Circle pressed")
        elif event.code == BTN_TRIANGLE:
            print("Triangle pressed")
        elif event.code == BTN_SQUARE:
            print("Square pressed")
        elif event.code == BTN_R1:
            print("R1 pressed")
        elif event.code == BTN_R2:
            print("R2 pressed") 
        elif event.code == BTN_L1:
            print("L1 pressed")
        elif event.code == BTN_L2:
            print("L2 pressed")
        elif event.code == BTN_R3:
            print("R3 pressed")

        elif event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_HAT0Y:
                if event.value == -1:
                    print("D-pad up")
                elif event.value == 1:
                    print("D-pad down")

            elif event.code == ecodes.ABS_HAT0X:
                if event.value == -1:
                    print("D-pad left")
                elif event.value == 1:
                    print("D-pad right")