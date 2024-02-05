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

# Create a player at the center of the screen
player_velocity = 5
player = pygame.Rect((screen_width // 2), (screen_height // 2), 45, 55)

# Load the rocket image
rocket_image = pygame.image.load("Assets/rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (45, 55))  # Resize if needed

# Background image
background_image = pygame.image.load('Assets/background.png')

# Define font
font = pygame.font.Font("Fonts/Pixel.ttf", 30)

# Button Rectangle
button = pygame.Rect(1236, 824, 300, 40)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(fps)

