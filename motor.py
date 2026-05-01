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


#Seigir mótor að fara áfram
def forward():
    send_motors(100,-100)


#Seigir mótor að fara tilbaka
def backwards():
    send_motors(-100, 100)


#Seigir mótor að fara til hægri
def right():
    send_motors(100, 0)


#Seigir mótor að fara til vinstri
def left():
    send_motors(0, -100)


#Seigir mótor að stoppa
def stop():
    send_motors(0, 0)

stop()
