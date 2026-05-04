import threading
import servo

lock = threading.Lock()
SRF02_data = {"left": None, "right": None}
Button_Press = {"state":False}
servos = [0,1]
servo.servo_init(servos)