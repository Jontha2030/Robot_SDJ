#import SRF02 as distanceSensors
#import servo as servoMotors
from motor import send_motors, forward, backwards, right, left, stop
import time
import pygame


pygame.init()
screen = pygame.display.set_mode((300, 300))  # needed for keyboard input

running = True
while running:
    # Handle events (VERY important)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                stop()
                running = False

    # Check held keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        forward()

    elif keys[pygame.K_DOWN]:
        backwards()

    elif keys[pygame.K_RIGHT]:
        right()

    elif keys[pygame.K_LEFT]:
        left()


pygame.quit()