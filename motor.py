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

def check_speed(speed):
    if speed >= 240:
        return 240
    else:
        return speed
#Seigir mótor að fara áfram
def forward(speed):
    speed = check_speed(speed)
    send_motors(speed + 15,-speed)


#Seigir mótor að fara tilbaka
def backwards(speed):
    speed = check_speed(speed)
    send_motors(-(speed + 15), speed)


#Seigir mótor að fara til hægri
def right(speed, hard_turn):
    speed = check_speed(speed)
    if hard_turn:
        send_motors(speed + 15,speed)
    else:
        send_motors(speed, 0)


#Seigir mótor að fara til vinstri
def left(speed, hard_turn):
    speed = check_speed(speed)
    if hard_turn:
        send_motors(-(speed + 15),-speed)
    else:
        send_motors(0, -speed)
        


#Seigir mótor að stoppa
def stop():
    send_motors(0, 0)
