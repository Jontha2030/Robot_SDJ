import time
from adafruit_servokit import ServoKit

# Virkjar PCA9685 chippinn sem er víst með 8 channels
kit = ServoKit(channels=8)

# Skilgreina í hvaða númer servo'arnir eru tengdir á borðinu
# eru frá 0-7 (8 pláss/channels)
servo_1 = 0
servo_2 = 1

# Fall sem snýr völdum servo mótor, valinn snúning
def move_servo(servo_nr, target_angle, speed=1):
    start_angle = kit.servo[servo_nr].angle # Sækji upphafsstöðu
    step = speed if start_angle > target_angle else -speed # Athugar hvort hann eigi að snúa til hægri eða vinstri
    for angle in range(start_angle, target_angle, step):
        print(angle)
        kit.servo[servo_nr].angle = angle
        time.sleep(0.02)
            
    
    return 0


def move_servos():
    
    
    return 0


def testing_servos():
    move_servo(0,10,1)
    
    return 0
