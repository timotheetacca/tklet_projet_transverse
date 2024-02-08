import pygame
import sys
import math
from trajectory import draw_trajectory, calculate_trajectory, draw_aim
from level import level

pygame.init()

# Set up the window
screen_width, screen_height =  1536, 864
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Efreispace")

transparent_surface_planet = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

#Set the cursor image and scale it to cursor size
cursor_image = pygame.image.load("Assets/Cursor/cursor_still.png")
cursor_image = pygame.transform.scale(cursor_image, (32, 32))

pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
fps = 120  # Set FPS rate for frame rate
font = pygame.font.Font(None, 22)

deplacement_x = 0
deplacement_y = 0
circle_radius = 5
level_number = 1
circle_x = 864
circle_y = 0
time_step = 0
g = 9.81
v = 130
h = 0
alpha = 0

mouse_pressed = False
shooting_trajectory = False
level_completed=False

def debug():
    # Set and blit information (fps, time, etc...) in upper left corner
    fps_text = font.render(f"FPS: {round(clock.get_fps())}", True, (255, 255, 255))
    time_text = font.render(f"T: {time_step}", True, (255, 255, 255))
    position_text = font.render(
        f"x({round(time_step)}) : {circle_x} , y({round(time_step)}) : {screen_height - circle_y}", True,
        (255, 255, 255))
    mouse_texte = font.render(f"mouse(x)={round(mouse_x)}  mouse(y)={round(screen_height-mouse_y)}", True, (255, 255, 255))
    angle_text = font.render(f"angle={round(alpha)}°", True, (255, 255, 255))
    velocity_text = font.render(f"velocity:{round(v)}", True, (255, 255, 255))
    shooting_text= font.render(f"deplacement_x: {deplacement_x}   deplacement_y: {deplacement_y} ", True, (255, 255, 255))
    velocity_augment_text = font.render(f"added  velocity: {deplacement_x / 7} + {-deplacement_y / 7}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 25))
    screen.blit(position_text, (10, 45))
    screen.blit(mouse_texte, (10, 65))
    screen.blit(angle_text, (10, 85))
    screen.blit(time_text, (10, 5))
    screen.blit(shooting_text, (10, 105))
    screen.blit(velocity_augment_text, (10, 125))
    screen.blit(velocity_text, (10,145))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse press events
            if event.button == 1:
                # Blit the hold cursor image and scale it
                cursor_image = pygame.image.load("Assets/Cursor/cursor_hold.png")
                cursor_image = pygame.transform.scale(cursor_image, (32, 32))

                mouse_pressed = True
                position_initiale_x, position_initiale_y = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # Blit the still cursor image and scale it
                cursor_image = pygame.image.load("Assets/Cursor/cursor_still.png")
                cursor_image = pygame.transform.scale(cursor_image, (32, 32))

                mouse_pressed = False
                shooting_trajectory = True
                level_completed = False

    screen.fill((0, 0, 0))

    # Get the mouse x and y
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate v continuously while mouse button is pressed
    if mouse_pressed:
        deplacement_x = position_initiale_x - mouse_x
        deplacement_y = position_initiale_y - mouse_y

        #Calculate the vector from the ball to the mouse
        vector_mouse = math.sqrt(mouse_x ** 2 + (screen_height-mouse_y) ** 2)

        #Calculate the angle between the x-axis
        alpha = math.degrees(math.acos(mouse_x / vector_mouse))

        # Get a velocity from the mouse deplacement
        v = 40 + deplacement_x / 10 - deplacement_y / 10

    # Projectile motion loop
    if shooting_trajectory == True:
        # Reset timer and position for shooting
        clock = pygame.time.Clock()
        circle_x = 0
        circle_y = 864
        time_step = 0

        while 0 <= circle_x <= screen_width and  0 <= (screen_height - circle_y) and level_completed==False:
            screen.fill((0, 0, 0))


            orbit_radius, position = level(level_number, screen, transparent_surface_planet)

            # Call the draw_trajectory function from trajectory.py
            circle_x, circle_y = draw_trajectory(screen, g, v, h, alpha, time_step, circle_radius, screen_height, (255, 255, 255))
            debug()
            pygame.display.update()
            time_step += clock.tick(fps) / 180  # Increment time step for the next iteration

            # Check if the projectile enters the planet's orbit
            if (circle_x - position[0]) ** 2 + (circle_y - position[1]) ** 2 <= orbit_radius ** 2:
                shooting_trajectory = False  # Stop shooting trajectory
                level_completed = True
                level_number += 1


        shooting_trajectory = False
        # Reset the mouse position to avoid angle error on the next throw
        pygame.mouse.set_pos(screen_width//2, screen_height//2)
        transparent_surface_planet.fill((0, 0, 0))

    else:
        # Display aiming trail if the player isn't shooting
        screen.fill((0, 0, 0))
        level(level_number, screen, transparent_surface_planet)
        debug()

        # Blit the cursor image
        screen.blit(cursor_image,(mouse_x, mouse_y))

        # Calculate the number of dots depending on the mouse x and y
        distance= 25-int(((mouse_x)*0.005))
        draw_aim(screen, g, v, h, alpha, time_step, 5, screen_height, distance)

    pygame.display.flip()  # Update the display