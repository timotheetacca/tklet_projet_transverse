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

circle_radius = 5
circle_x = 0
circle_y = 0
time_step = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.draw.circle(screen, (255, 255, 255, 50), (circle_x, circle_y), circle_radius)

    # Update circle position
    circle_x = int(x(time_step, 100, 90))
    circle_y = screen_height - int(y(time_step, 9.81, 100, 0, 45))

    # Update the display
    pygame.display.update()

    # Pause for 0.5 seconds
    pygame.time.delay(100)  # Delay in milliseconds

    # Control the frame rate
    clock.tick(fps)

    # Increment the time step for the next iteration
    time_step += 1
    print(f"y({time_step}) = {circle_y} - x({time_step}) = {circle_x}")

    if circle_y > screen_height:
        pygame.quit()
