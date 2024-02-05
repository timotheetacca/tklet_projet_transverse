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
font = pygame.font.Font(None, 36)

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

    # Calculate the time difference since the last frame
    time_diff = clock.tick(fps) / 1000.0  # Convert to seconds

    # Update circle position based on the time difference
    circle_x = int(x(time_step, 100, 45))
    circle_y = screen_height - int(y(time_step, 9.81, 100, 0, 45))

    # Draw the circle on the screen
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.circle(screen, (255, 255, 255, 50), (circle_x, circle_y), circle_radius)

    # Increment the time step for the next iteration
    time_step += time_diff

    #Show FPS
    fps_text = font.render(f"FPS: {round(clock.get_fps(), 1)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    # Update the display
    pygame.display.update()
