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


# Fall sem snýr völdum servo mótor, valinn snúning
def move_servo(servo_nr, target_angle, speed=1):
    start_angle = kit.servo[servo_nr].angle # Sækji upphafsstöðu
    #print("Start angle:", start_angle) #----DEBUG
    #print("Target angle:", target_angle) #----DEBUG
    step = speed if start_angle < target_angle else -speed # Athugar hvort hann eigi að snúa til hægri eða vinstri
    #print("Step size:", step) #----DEBUG
    for angle in range(int(start_angle), int(target_angle), int(step)):
        #print(angle) #----DEBUG
        kit.servo[servo_nr].angle = angle
        time.sleep(0.02)


    return 0


def move_servos():


    return 0


def testing_servos(servos):
    #servo_init(servos)
    while True:
        angle = int(input("Angle(0-180):"))
        speed = int(input("Speed(<10?):"))
        move_servo(servos[1],angle,speed)

    return 0

#testing_servos(servos)


def selfturning_servos():

    kit.servo[0].angle = 90
    kit.servo[1].angle = 90


    while True:
        for angle in range(90, 0, 10):
            kit.servo[0].angle = angle
            kit.servo[1].angle = angle
            time.sleep(0.05)
            
        for angle in range(0, 90, 10):
            kit.servo[0].angle = angle
            kit.servo[1].angle = angle
            time.sleep(0.05)
        

selfturning_servos()

  


