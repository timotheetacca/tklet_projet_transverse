import pygame
import sys
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
time_step_aim = 0
g = 9.81
v = 100
h = 0
alpha = 45

spacebar_pressed = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Check for key press events
            if event.key == pygame.K_SPACE:
                spacebar_pressed = True  # Set spacebar_pressed to True when spacebar is pressed

    draw_aim(screen, g,v,h,alpha,time_step,screen_height,5,circle_radius)

    if spacebar_pressed == True:
        # Reset timer for shooting
        clock = pygame.time.Clock()
        circle_x = 864
        circle_y = 0
        time_step = 0
        while 0 <= circle_x <= screen_width and  0 <= (screen_height-circle_y)  <= screen_height:

            # Call the draw_trajectory function from trajectory.py
            circle_x,circle_y=draw_trajectory(screen, g, v, h, alpha, time_step, circle_radius, screen_height,(255,255,255))

            fps_text = font.render(f"FPS: {round(clock.get_fps())}", True, (255, 255, 255))
            time_text = font.render(f"T: {time_step}", True, (255, 255, 255))
            position_text = font.render(f"x({round(time_step)}) : {circle_x} , y({round(time_step)}) : {screen_height - circle_y}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 20))
            screen.blit(position_text, (10, 40))
            screen.blit(time_text, (10, 0))

            pygame.display.update()

            time_step += clock.tick(fps) / 300  # Increment time step for the next iteration

        spacebar_pressed = False

