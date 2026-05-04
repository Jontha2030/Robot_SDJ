import time
from adafruit_servokit import ServoKit

# Virkjar PCA9685 chippinn sem er víst með 8 channels
kit = ServoKit(channels=8)

# Skilgreina í hvaða númer servo'arnir eru tengdir á borðinu
# eru frá 0-7 (8 pláss/channels)
servos = [0, 1]

# Lætur servoa snúa í miðju
def servo_init(servos):
    for servo_nr in servos:
        #print("test", servo_nr) #----DEBUG
        kit.servo[servo_nr].angle = 90


def selfturning_servos():
    while True:

        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        
        time.sleep(0.01)

        for angle in range(120, -10, -30):
            kit.servo[0].angle = angle
            kit.servo[1].angle = 90 + (90-angle)
            time.sleep(0.05)
            
 
        kit.servo[0].angle = 0
        kit.servo[1].angle = 180
        time.sleep(0.01)

        for angle in range(0, 130, 30):
            kit.servo[0].angle = angle
            kit.servo[1].angle = 90 + (90-angle)
            time.sleep(0.05)
        




  


