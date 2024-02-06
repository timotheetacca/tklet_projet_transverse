import pygame
import sys
import math
from pygame.locals import *

pygame.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Efreispace")

clock = pygame.time.Clock()
fps = 120  # Set FPS rate for frame rate

def y(t, g, v, h, alpha):
    return (-1/2) * g * t**2 + v * math.sin(math.radians(alpha)) * t + h

def x(t, v, alpha):
    return v * math.cos(math.radians(alpha)) * t

circle_x, circle_y = 0, 0
time_step = 0

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
        elif event.type == pygame.MOUSEMOTION:
            time_step = 0
            mouse_x, mouse_y = pygame.mouse.get_pos()

    angle = math.degrees(math.atan2(screen_height - mouse_y, mouse_x))
    circle_x = int(x(time_step, 100, angle))
    circle_y = screen_height - int(y(time_step, 9.81, 100, 0, angle))

    # Draw background
    screen.fill((0, 0, 0))

    # Draw the circle
    pygame.draw.circle(screen, (255, 255, 255, 50), (circle_x, circle_y), 5)

    # Update the display
    pygame.display.update()

    # Pause for 0.5 seconds
    pygame.time.delay(100)  # Delay in milliseconds

    # Control the frame rate
    clock.tick(fps)

    # Increment the time step for the next iteration
    time_step += 1
