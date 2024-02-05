
import pygame
import sys
import math

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

#Make the trajectory show only once
first_time=True
# Clear the screen
screen.fill((0, 0, 0))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    if first_time:
        for i in range(20):
            circle_x = int(x(i, 100, 45))
            circle_y = int(y(i, 9.81, 100, 0, 45))
            pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 5)
            print(f"y({i}) = {y(i, 9.81, 100, 0, 45)} - x({i}) = {x(i, 100, 45)}")
        first_time = False

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(fps)
