from speaker import Speaker
import SRF02
import time
import threading
import servo

lock = threading.Lock()
SRF02_data = {"left": None, "right": None}
servos = [0,1]
servo.servo_init(servos)