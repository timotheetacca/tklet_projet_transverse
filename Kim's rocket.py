import pygame
import sys
import math
from pygame.locals import *

pygame.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Efrei Space")

rocket_image = pygame.image.load("rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (75, 75))  # Resize if needed
planet_image = pygame.image.load("planet.png")
planet_image = pygame.transform.scale(planet_image, (300, 300))  # Resize if needed
background_image = pygame.image.load('background.png')

clock = pygame.time.Clock()
fps = 120

class Planet:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)

class Rocket:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
    def update(self, time, velocity, angle):
        self.x = int(x(time, velocity, angle))
        self.y = screen_height - int(y(time, 9.81, velocity, 0, angle))
        return self.x, self.y

def x(time, velocity, angle):
    return velocity * math.cos(math.radians(angle)) * time
def y(time, g, velocity, height, angle):
    return (-1/2) * g * time**2 + velocity * math.sin(math.radians(angle)) * time + height

planet = Planet((1250, 250), 75, (255, 0, 0))
rocket = Rocket(0, screen_height, 10, (255, 255, 255))
time_step = 0

rocket_launch = False
run = True
while run:
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key== K_ESCAPE:
                run=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rocket_launch:
                rocket.x = 0
                rocket.y = screen_height
                time_step = 0
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dy = mouse_y - screen_width
                dx = mouse_x - screen_height
                angle = math.degrees(math.atan2(rocket.y - mouse_y, mouse_x - rocket.x))
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dy = mouse_y - screen_width
                dx = mouse_x - screen_height
                angle = math.degrees(math.atan2(rocket.y - mouse_y, mouse_x - rocket.x))
                rocket_launch = True

    # Calculate the time difference since the last frame
    time_diff = clock.tick(fps) / 1000.0  # Convert to seconds

    screen.blit(background_image, (0, 0))
    screen.blit(planet_image, (1250 - planet_image.get_width() // 2, 250 - planet_image.get_height() // 2))

    if rocket_launch:
        screen.blit(background_image, (0, 0))
        screen.blit(planet_image, (1250 - planet_image.get_width() // 2, 250 - planet_image.get_height() // 2))
        rocket_position = rocket.update(time_step, 100, angle)
        screen.blit(rocket_image, (rocket_position[0] - rocket_image.get_width() // 2, rocket_position[1] - rocket_image.get_height() // 2))

    # Increment the time step for the next iteration
    time_step += time_diff

    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()