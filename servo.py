import time
from adafruit_servokit import ServoKit
from __init__ import Button_Press, lock

# Virkjar PCA9685 chippinn sem er víst með 8 channels
kit = ServoKit(channels=8)

# Skilgreina í hvaða númer servo'arnir eru tengdir á borðinu
# eru frá 0-7 (8 pláss/channels)
servos = [0, 1, 3]

# Lætur servoa snúa í miðju
def servo_init(servos):
    for servo_nr in servos:
        #print("test", servo_nr) #----DEBUG
        kit.servo[servo_nr].angle = 90


def cameraservoplus():
    kit.servo[3].angle += 30

    if kit.servo[3].angle >= 180:
        kit.servo[3].angle = 180

    if kit.servo[3].angle <= 0:
        kit.servo[3].angle = 0
    

def cameraservominus():
    kit.servo[3].angle -= 30

    if kit.servo[3].angle >= 180:
        kit.servo[3].angle = 180

    if kit.servo[3].angle <= 0:
        kit.servo[3].angle = 0





#Fall sem lætur servos snúa sjálfkrafa
def selfturning_servos():
    servo_init(servos)
    while True:
        with lock:
            button_state = Button_Press["state"]
            
        if button_state:
            print("Slekk á servo'um")
            break

        #Lætur þá snúa beint áfram
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        
        time.sleep(0.01)
        
        #For lykkja sem lætur þá snúa sér út
        for angle in range(120, -10, -30):
            kit.servo[0].angle = angle
            kit.servo[1].angle = 90 + (90-angle)
            time.sleep(0.05)
            
        
        #lætur þá snúa út
        kit.servo[0].angle = 0
        kit.servo[1].angle = 180
        time.sleep(0.01)
        

        #For lykkja sem lætur þá snúa sér inn
        for angle in range(0, 130, 30):
            kit.servo[0].angle = angle
            kit.servo[1].angle = 90 + (90-angle)
            time.sleep(0.05)
        




  


