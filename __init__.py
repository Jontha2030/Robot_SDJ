import threading
from adafruit_servokit import ServoKit

lock = threading.Lock()
SRF02_data = {"left": None, "right": None}
Button_Press = {"state":False}

kit = ServoKit(channels=8)