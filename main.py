import pygame
import sys
from trajectory import draw_trajectory

pygame.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Efreispace")

clock = pygame.time.Clock()
fps = 120  # Set FPS rate for frame rate
font = pygame.font.Font(None, 36)

circle_radius = 5
circle_x = 0
circle_y = 0
time_step = 0
g = 9.81
v = 100
h = 0
alpha = 45

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # Fill the screen with black

    # Call the draw_trajectory function from trajectory.py
    draw_trajectory(screen, g, v, h, alpha, time_step, circle_radius, screen_height)

    # Show FPS
    fps_text = font.render(f"FPS: {round(clock.get_fps(), 1)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.update()

    time_step += clock.tick(fps) / 1000.0  # Increment time step for the next iteration