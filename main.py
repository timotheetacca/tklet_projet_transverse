import pygame
from trajectory import draw_aim
import math
from trajectory_simulation import TrajectorySimulation

pygame.init()

# Set up the window
screen_width, screen_height =  1536, 864
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Efreispace")

fps = 120  # Set FPS rate for frame rate

# Initialize TrajectorySimulation instance
trajectory_simulation = TrajectorySimulation()

level_number = 1
alpha = 0
time_step=0
circle_x = 864
circle_y = 0
circle_radius = 5
g = 9.81
v=130
h = 0

mouse_pressed = False
shooting_trajectory = False
stop_level = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pressed = True
                position_initiale_x, position_initiale_y = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pressed = False
                shooting_trajectory = True
                stop_level = False

    screen.fill((0, 0, 0))

    # Get the mouse x and y
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate v continuously while mouse button is pressed
    if mouse_pressed:
        deplacement_x = position_initiale_x - mouse_x
        deplacement_y = position_initiale_y - mouse_y

        # Calculate the vector from the ball to the mouse
        vector_mouse = math.sqrt(mouse_x ** 2 + (screen_height - mouse_y) ** 2)

        # Calculate the angle between the x-axis
        alpha = math.degrees(math.acos(mouse_x / vector_mouse))

        # Get a velocity from the mouse deplacement
        v = 40 + deplacement_x / 10 - deplacement_y / 10

    # Projectile motion loop

    if shooting_trajectory:
        shooting_trajectory, level_number = trajectory_simulation.projectile_motion(screen, circle_x, circle_y, g , v, h, alpha, level_number)
    else:
        trajectory_simulation.projectile_aim(screen, g, v, h, alpha, time_step, screen_height, mouse_x, level_number)

    pygame.display.flip()  # Update the display
