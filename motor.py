import time
import smbus



#Sendir boð til mótor
def send_motors(m1, m2):
    I2C_ADDRESS = 0x50
    bus = smbus.SMBus(1)

    m1_speed = abs(m1)
    m1_sign = 0 if m1 >= 0 else 1

    m2_speed = abs(m2)
    m2_sign = 0 if m2 >= 0 else 1

    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)


#Skoðar hvort hraði fari yfir leyfinlegan hraða
def check_speed(speed):
    if speed >= 240:
        return 240
    else:
        return speed
    
#Seigir mótor að fara áfram
def forward(speed):
    speed = check_speed(speed)
    send_motors(speed + 8,-speed-14)


#Seigir mótor að fara afturábaka
def backwards(speed):
    speed = check_speed(speed)
    send_motors(-(speed + 14), speed-7)


#Seigir mótor að fara til hægri
def right(speed):
    speed = check_speed(speed)
    send_motors((speed + 15),speed)


#Seigir mótor að fara til vinstri
def left(speed):
    speed = check_speed(speed)
    send_motors(-(speed + 15),-speed)


#Seigir mótor að stoppa
def stop():
    send_motors(0, 0)
