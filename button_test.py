from evdev import InputDevice, ecodes

dev = InputDevice("/dev/input/event4")
print("Press D-pad or L3. Ctrl+C to quit")

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print("KEY", event.code, event.value)

    elif event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_HAT0X:
            print("DPAD_X", event.value)  # -1 left, 1 right, 0 release
        elif event.code == ecodes.ABS_HAT0Y:
            print("DPAD_Y", event.value)  # -1 up, 1 down, 0 release
