import pygame
import sys
import math
from trajectory import draw_trajectory, calculate_trajectory, draw_aim

pygame.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Efreispace")

clock = pygame.time.Clock()
fps = 120  # Set FPS rate for frame rate
font = pygame.font.Font(None, 22)

circle_radius = 5
circle_x = 864
circle_y = 0
time_step = 0
g = 9.81
v = 130
h = 0
alpha = 50

spacebar_pressed = False
# Reset the mouse position to avoid angle error on the next throw
pygame.mouse.set_pos(150, 680)


# Create a surface with the desired transparency
transparent_surface_planet = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
orbit=pygame.draw.circle(transparent_surface_planet, (255, 255, 255, 100), (screen_width//2, screen_height//2), 120)
pygame.draw.circle(transparent_surface_planet, (255, 255, 255, 250), (screen_width//2, screen_height//2), 45)

def f3():
    # Set and blit information (fps, time, etc...) in upper left corner
    fps_text = font.render(f"FPS: {round(clock.get_fps())}", True, (255, 255, 255))
    time_text = font.render(f"T: {time_step}", True, (255, 255, 255))
    position_text = font.render(
        f"x({round(time_step)}) : {circle_x} , y({round(time_step)}) : {screen_height - circle_y}", True,
        (255, 255, 255))
    mouse_texte = font.render(f"mouse(x)={round(mouse_x)}  mouse(y)={round(mouse_y)}", True, (255, 255, 255))
    angle_text = font.render(f"angle={round(alpha)}°", True, (255, 255, 255))
    velocity_text = font.render(f"v:{round(v)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 20))
    screen.blit(position_text, (10, 40))
    screen.blit(mouse_texte, (10, 60))
    screen.blit(angle_text, (10, 80))
    screen.blit(time_text, (10, 0))
    screen.blit(velocity_text, (10,100))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Check for key press events
            if event.key == pygame.K_SPACE:
                spacebar_pressed = True  # Set spacebar_pressed to True when spacebar is pressed

    # Get the mouse x and y
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculates the x and y coordinates of the mouse relative to the bottom left corner
    dy = mouse_y - screen_width
    dx = mouse_x - screen_height

    # Compute the angle between two points the position of a rocket and the mouse cursor position
    alpha = math.degrees(math.atan2(circle_y - mouse_y + 2000, mouse_x))

    # Adapt the speed with the mouse position (⚠ Prototype velocity, it won't stay like this)
    v = 40 + mouse_x / 25 + (screen_height - mouse_y) / 15

    continue_shooting = True  # Flag to control shooting continuation

    if spacebar_pressed:
        # Reset timer and position for shooting
        clock = pygame.time.Clock()
        circle_x = 864
        circle_y = 0
        time_step = 0
        while 0 <= circle_x <= screen_width and 0 <= (screen_height - circle_y) <= screen_height and continue_shooting:
            screen.fill((0, 0, 0))

            # Blit the transparent surface onto the main screen
            screen.blit(transparent_surface_planet, (0, 0))

            # Call the draw_trajectory function from trajectory.py
            circle_x, circle_y = draw_trajectory(screen, g, v, h, alpha, time_step, circle_radius, screen_height, (255, 255, 255))
            f3()
            pygame.display.update()

            # Check for collision with the orbit
            orbit_center_x, orbit_center_y = screen_width // 2, screen_height // 2
            distance_to_orbit = math.sqrt((circle_x - orbit_center_x) ** 2 + (circle_y - orbit_center_y) ** 2)
            if distance_to_orbit <= 120 + circle_radius:  # Radius of orbit + radius of the ball
                spacebar_pressed = False
                continue_shooting = False  # Set flag to stop shooting

            time_step += clock.tick(fps) / 180  # Increment time step for the next iteration
        # Reset the mouse position to avoid angle error on the next throw
        pygame.mouse.set_pos(150, 680)

    else:
        # If the player isn't shooting, it will show the aiming trail
        screen.fill((0, 0, 0))
        f3()

        # Blit the transparent surface onto the main screen
        screen.blit(transparent_surface_planet, (0, 0))

        draw_aim(screen, g, v, h, alpha, time_step, 5, screen_height, 25)

    pygame.display.flip()  # Update the display
