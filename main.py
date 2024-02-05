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
frame_time = 0

<<<<<<< HEAD
# Create a separate surface for the trail
trail_surface = pygame.Surface((screen_width, screen_height))

=======
>>>>>>> origin/main
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate the time difference since the last frame
    current_time = pygame.time.get_ticks()
    time_diff = current_time - frame_time
    frame_time = current_time

    # Update circle position based on the time difference
    circle_x = int(x(time_step + time_diff / 1000, 100, 45))
    circle_y = screen_height - int(y(time_step + time_diff / 1000, 9.81, 100, 0, 45))

    # Draw the circle on the trail surface
    pygame.draw.circle(trail_surface, (255, 255, 255, 50), (circle_x, circle_y), circle_radius)

    # Update the display
    screen.blit(trail_surface, (0, 0))  # Blit the trail surface onto the screen
    pygame.display.update()

    # Control the frame rate
    clock.tick(fps)

    # Increment the time step for the next iteration
    time_step += time_diff / 1000

    # Clear the trail surface after each time step
    trail_surface.fill((0, 0, 0, 0))