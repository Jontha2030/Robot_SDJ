import SRF02 as distanceSensors
import servo as servoMotors

from speaker import Speaker
import time

# Frumstilla speaker
speaker = Speaker()

# Þegar bíllinn fer í gang — spila lag
print("Bíllinn fer í gang!")
speaker.play()

# ... afgangur af main loop ...
# (bíllinn keyrir, gerir hluti, etc.)

# Til að stöðva (ef þarf):
# speaker.stop()
