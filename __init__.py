from speaker import Speaker
import SRF02
import time
import threading
import servo

lock = threading.Lock()
SRF02_data = {"left": None, "right": None}
servo.servo_init()