import threading

lock = threading.Lock()
SRF02_data = {"left": None, "right": None}
Button_Press = {"state":False}
First_SRF02_run = {"state":True}