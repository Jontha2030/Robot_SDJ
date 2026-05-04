import threading
from SRF02 import distance_scan

lock = threading.Lock()
SRF02thread = threading.Thread(target=distance_scan, daemon=True) # Búum til þráð fyrir fjarlægðarskynjarana sem keyrir alltaf
SRF02thread.start()
SRF02_data = {"left": None, "right": None}
Button_Press = {"state":False}