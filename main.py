#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
import time
from pynput import keyboard

pressed = set()

def on_press(key):
    pressed.add(key)

    if key == keyboard.Key.up:
        forward()
    elif key == keyboard.Key.down:
        backwards()
    elif key == keyboard.Key.right:
        right()
    elif key == keyboard.Key.left:
        left()

    # press q to quit
    try:
        if key.char == "q":
            stop()
            return False
    except AttributeError:
        pass

def on_release(key):
    pressed.discard(key)

    if key in [
        keyboard.Key.up,
        keyboard.Key.down,
        keyboard.Key.right,
        keyboard.Key.left
    ]:
        stop()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

stop()