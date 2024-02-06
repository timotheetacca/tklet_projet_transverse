import pygame
import sys
import math
from pygame.locals import *

pygame.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Efrei Space")

# Load images and set their scales
rocket_image = pygame.image.load("rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (125, 125))  # Resize if needed
planet_image = pygame.image.load("planet.png")
planet_image = pygame.transform.scale(planet_image, (200, 200))
asteroid_image = pygame.image.load("asteroid.png")
asteroid_image = pygame.transform.scale(asteroid_image, (175, 125))
astronaut_image = pygame.image.load("astronaut.png")
astronaut_image = pygame.transform.scale(astronaut_image, (175, 200))
squelette_image = pygame.image.load("squelette.png")
squelette_image = pygame.transform.scale(squelette_image, (100, 115))
orbit_image = pygame.image.load("orbit.png")
orbit_image = pygame.transform.scale(orbit_image, (350, 350))
lose_image = pygame.image.load("lose.png")
lose_image = pygame.transform.scale(lose_image, (700, 350))
win_image = pygame.image.load("win.png")
win_image = pygame.transform.scale(win_image, (800, 350))
background_image = pygame.image.load('background.png')

# Initialize clock and frames per second
clock = pygame.time.Clock()
fps = 120

# Define a class for the planet
class Planet:
    # Initialize planet properties
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
    # Draw the planet on the game surface
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
    # Update the rocket's position based on time, velocity, and launch angle
    def update(self, time, velocity, angle):
        self.x = int(x(time, velocity, angle))
        self.y = screen_height - int(y(time, 9.81, velocity, 0, angle))
        return self.x, self.y

# Define functions for trajectory calculations
def x(time, velocity, angle):
    return velocity * math.cos(math.radians(angle)) * time
def y(time, g, velocity, height, angle):
    return (-1/2) * g * time**2 + velocity * math.sin(math.radians(angle)) * time + height

# Create Planet and Rocket
planet = Planet((1250, 250), 75, (255, 0, 0))
rocket = Rocket(0, screen_height, 10, (255, 255, 255))

# Initialize variables for the trail of points
circle_x, circle_y = 0, 0
nb_astronauts = 0
time_step = 0

# Initialize Boolean variables
draw_trail = True
rocket_launch = False
rocket_reaching_orbit = False
lose=False
rocket_collision = False

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            # Exit the game by pressing ESC
            if event.key== K_ESCAPE:
                run=False
            if event.key==K_SPACE:
                rocket_reaching_orbit = False
        # Track mouse motion
        elif event.type == pygame.MOUSEMOTION and not rocket_launch:
            # Reset time_step and mouse coordinate positions to reinitialize the trail of points
            time_step = 0
            mouse_x, mouse_y = pygame.mouse.get_pos()
        # Event handling: mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rocket_launch:
                # If rocket is already launched, reset rocket position and time_step
                rocket.x = 0
                rocket.y = screen_height
                time_step = 0
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dy = mouse_y - screen_width
                dx = mouse_x - screen_height
                # Compute the angle between two points the position of a rocket and the mouse cursor position
                angle = math.degrees(math.atan2(rocket.y - mouse_y, mouse_x - rocket.x))
            else:
                # Launch the rocket based on mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dy = mouse_y - screen_width
                dx = mouse_x - screen_height
                angle = math.degrees(math.atan2(rocket.y - mouse_y, mouse_x - rocket.x))
                rocket_launch = True

    # Calculate trail points coordinates based on mouse position
    angle_trajectory = math.degrees(math.atan2(screen_height - mouse_y, mouse_x))
    circle_x = int(x(time_step, 100, angle_trajectory))
    circle_y = screen_height - int(y(time_step, 9.81, 140, 0, angle_trajectory))

    # Calculate the time difference since the last frame
    time_diff = clock.tick(fps) / 1000.0  # Convert to seconds

    # Draw background & planet and its orbit
    screen.blit(background_image, (0, 0))
    screen.blit(planet_image, (1250 - planet_image.get_width() // 2, 250 - planet_image.get_height() // 2))
    screen.blit(orbit_image, (1250 - orbit_image.get_width() // 2, 250 - orbit_image.get_height() // 2))
    screen.blit(asteroid_image, (750 - asteroid_image.get_width() // 2, 500 - asteroid_image.get_height() // 2))

    # Draw trail of points if enabled
    if draw_trail and not rocket_launch and not lose :
        pygame.draw.circle(screen, (255, 255, 255, 128), (circle_x, circle_y), 5)

    distance_to_orbit = math.sqrt((rocket.x - 1250) ** 2 + (rocket.y - 250) ** 2)
    if distance_to_orbit <= (rocket.radius + orbit_image.get_width() // 2):
        rocket_reaching_orbit = True

    distance_to_asteroid = math.sqrt((rocket.x - 750) ** 2 + (rocket.y - 500) ** 2)
    if distance_to_asteroid <= (rocket.radius + asteroid_image.get_width() // 2):
        rocket_collision = True

    # Draw rocket if enabled
    if rocket_launch and not lose:
        # Disable drawing the trail of points while the rocket is in motion
        draw_trail = False
        rocket_position = rocket.update(time_step, 140, angle)
        screen.blit(rocket_image, (rocket_position[0] - rocket_image.get_width() // 2, rocket_position[1] - rocket_image.get_height() // 2))
        # If rocket reaches the bottom, reset launch conditions
        if rocket_position[1] > screen_height:
            rocket_launch = False
            draw_trail = True

    if rocket_collision:
        nb_astronauts+=1

    if nb_astronauts==0:
        screen.blit(astronaut_image, (1450 - astronaut_image.get_width() // 2, 800 - astronaut_image.get_height() // 2))
        screen.blit(astronaut_image, (1350 - astronaut_image.get_width() // 2, 800 - astronaut_image.get_height() // 2))
        screen.blit(astronaut_image, (1250 - astronaut_image.get_width() // 2, 800 - astronaut_image.get_height() // 2))
    elif nb_astronauts==1:
        screen.blit(astronaut_image, (1450 - astronaut_image.get_width() // 2, 800 - astronaut_image.get_height() // 2))
        screen.blit(astronaut_image, (1350 - astronaut_image.get_width() // 2, 800 - astronaut_image.get_height() // 2))
        screen.blit(squelette_image, (1250 - squelette_image.get_width() // 2, 775 - squelette_image.get_height() // 2))
    elif nb_astronauts==2:
        screen.blit(astronaut_image, (1450 - astronaut_image.get_width() // 2, 800 - astronaut_image.get_height() // 2))
        screen.blit(squelette_image, (1350 - squelette_image.get_width() // 2, 775 - squelette_image.get_height() // 2))
        screen.blit(squelette_image, (1250 - squelette_image.get_width() // 2, 775 - squelette_image.get_height() // 2))
    elif nb_astronauts>=3:
        screen.blit(squelette_image, (1450 - squelette_image.get_width() // 2, 775 - squelette_image.get_height() // 2))
        screen.blit(squelette_image, (1350 - squelette_image.get_width() // 2, 775 - squelette_image.get_height() // 2))
        screen.blit(squelette_image, (1250 - squelette_image.get_width() // 2, 775 - squelette_image.get_height() // 2))
        lose=True

    if lose:
        screen.blit(lose_image, (screen_width//2 - lose_image.get_width() // 2, screen_height//2 - lose_image.get_height() // 2))

    if rocket_reaching_orbit:
        screen.blit(win_image, (screen_width//2 - win_image.get_width() // 2, screen_height//2 - win_image.get_height() // 2))

    # Update the display
    pygame.display.update()

    # Increment the time step for the next iteration
    time_step += time_diff

    # Update the display
    pygame.display.update()

    # Pause for a short time to control frame rate
    pygame.time.delay(100)

    # Control the frame rate
    clock.tick(fps)

    # Increment the time step for the next iteration
    time_step += 1

# Quit the game
pygame.quit()
sys.exit()