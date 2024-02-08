import pygame
import sys
import math

pygame.init()

# Set up the window
screen_width, screen_height =  1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Efrei Space")

clock = pygame.time.Clock()
fps = 120  # Set FPS rate for frame rate
font = pygame.font.Font(None, 22)

circle_radius = 5
circle_x = 100
circle_y = 764
time_step = 0
g = 9.81
v = 130
h = 0
angle = 50

def calculate_trajectory(g, v, h, angle, t, screen_height):
    new_circle_y = circle_y - int((-1/2) * g * t**2 + v * math.sin(math.radians(angle)) * t + h)
    new_circle_x = circle_x + int (v * math.cos(math.radians(angle)) * t)
    return new_circle_x, new_circle_y

def draw_aim(screen, g, v, h, angle, t, circle_radius,screen_height, distance,):
    for t in range(distance):
        new_circle_x, new_circle_y=calculate_trajectory(g, v, h, angle, t/2, screen_height)
        # Reduce the radius of the circle to make the aiming less and less visible
        pygame.draw.circle(screen, (250,250,250), (new_circle_x+20, new_circle_y-20), circle_radius-0.1*t)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the mouse x and y
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate angle between circle center and mouse position
    dx = circle_x - mouse_x
    dy = circle_y - mouse_y
    angle = abs(math.degrees(math.atan2(dy, dx)))

    # Clear the screen
    screen.fill((0, 0, 0))

    distance = 25 - int(((mouse_x) * 0.005))
    draw_aim(screen, g, v, h, angle, time_step, 5, screen_height, distance)

    # Display angle text
    angle_text = font.render(f"Angle: {round(angle)} degrees", True, (255, 255, 255))
    screen.blit(angle_text, (10, 10))

    pygame.display.update()
    clock.tick(fps)

