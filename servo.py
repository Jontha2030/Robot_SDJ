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
        kit.servo[servo_nr].angle = 90
        

# Fall sem snýr völdum servo mótor, valinn snúning
def move_servo(servo_nr, target_angle, speed=1):
    start_angle = kit.servo[servo_nr].angle # Sækji upphafsstöðu
    print("Start angle:", start_angle)
    step = speed if start_angle > target_angle else -speed # Athugar hvort hann eigi að snúa til hægri eða vinstri
    for angle in range(int(start_angle), int(target_angle), int(step)):
        print(angle)
        kit.servo[servo_nr].angle = angle
        time.sleep(0.02)


    return 0


def move_servos():


    return 0


def testing_servos(servos):
    servo_init(servos)
    move_servo(1,0,2)

    return 0

testing_servos(servos)
