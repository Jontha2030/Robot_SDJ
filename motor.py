import time
import smbus

I2C_ADDRESS = 0x50
bus = smbus.SMBus(1)


def send_motors(m1, m2):
    m1_speed = abs(m1)
    m1_sign = 0 if m1 >= 0 else 1

    m2_speed = abs(m2)
    m2_sign = 0 if m2 >= 0 else 1

    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)


def forward():
    send_motors(100, 100)


def backwards():
    send_motors(-100, -100)


def right():
    send_motors(100, 0)


def left():
    send_motors(0, 100)


def stop():
    send_motors(0, 0)