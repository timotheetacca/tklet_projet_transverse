import pygame
import sys
import math
from trajectory import draw_trajectory, calculate_trajectory, draw_aim

pygame.init()

# Set up the window
screen_width, screen_height =  1536, 864
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

def f3():
    # Set and blit information (fps, time, etc...) in upper left corner
    fps_text = font.render(f"FPS: {round(clock.get_fps())}", True, (255, 255, 255))
    time_text = font.render(f"T: {time_step}", True, (255, 255, 255))
    position_text = font.render(
        f"x({round(time_step)}) : {circle_x} , y({round(time_step)}) : {screen_height - circle_y}", True,
        (255, 255, 255))
    mouse_texte = font.render(f"mouse(x)={round(mouse_x)}  mouse(y)={round(mouse_y)}", True, (255, 255, 255))
    angle_text = font.render(f"ange={round(alpha)}°", True, (255, 255, 255))
    velocity_text = font.render(f"v:{round(v)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 25))
    screen.blit(position_text, (10, 45))
    screen.blit(mouse_texte, (10, 65))
    screen.blit(angle_text, (10, 85))
    screen.blit(time_text, (10, 5))
    screen.blit(velocity_text, (10,105))

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
    alpha = math.degrees(math.atan2(circle_y - mouse_y+2000, mouse_x ))

    # Adapt the speed with the mouse position (⚠ Prototype velocity, it won't stay like this)
    v = 40 + mouse_x / 22 + (screen_height - mouse_y) / 16

    if spacebar_pressed == True:
        # Reset timer and position for shooting
        clock = pygame.time.Clock()
        circle_x = 864
        circle_y = 0
        time_step = 0
        while 0 <= circle_x <= screen_width and  0 <= (screen_height - circle_y):
            screen.fill((0, 0, 0))

            # Call the draw_trajectory function from trajectory.py
            circle_x, circle_y = draw_trajectory(screen, g, v, h, alpha, time_step, circle_radius, screen_height, (255, 255, 255))
            f3()
            pygame.display.update()


            time_step += clock.tick(fps) / 180  # Increment time step for the next iteration
        spacebar_pressed = False
        # Reset the mouse position to avoid angle error on the next throw
        pygame.mouse.set_pos(150, 680)

    else:
        # If the player isn't shooting, it will show the aiming trail
        screen.fill((0, 0, 0))
        f3()
        distance= 25-int(((screen_width-mouse_x)*0.005))

        draw_aim(screen, g, v, h, alpha, time_step, 5, screen_height, distance)

    pygame.display.flip()  # Update the display
