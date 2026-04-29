import time
from adafruit_servokit import ServoKit

# Initialize the PCA9685 for 16 channels
kit = ServoKit(channels=16)

# Set the servo on channel 0 to 0 degrees
print("Moving to 0 degrees")
kit.servo[0].angle = 0
time.sleep(1)

