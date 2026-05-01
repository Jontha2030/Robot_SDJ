import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# For a servo, 1ms pulse = 0°, 2ms pulse = 180°
# At 50Hz, period = 20ms
# 1ms = 4915 counts, 2ms = 9830 counts (out of 65535)
pca.channels[3].duty_cycle = 4915  # should move to 0°
