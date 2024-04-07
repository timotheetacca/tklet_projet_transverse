import pygame.mixer
import math
from trajectory_simulation import TrajectorySimulation
from orbital_phase import OrbitalPhase
from slider import Slider
from save import update_save_information, update_level
from level_map import level_selection

pygame.init()
pygame.mixer.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Efreispace")

# Set up the cursor
cursor_image = pygame.image.load("Assets/Cursor/cursor_still.png")
cursor = pygame.transform.scale(cursor_image, (32, 32))
pygame.mouse.set_visible(False)

# Load a background image
background_image = pygame.image.load("Assets/Level/background_space.png")

# Music parameters
pygame.mixer.music.load("Assets/Music/musicTKLET.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

size_music_button = 90
green_music_button = pygame.image.load("Assets/Music/Green Music Button.png")
green_music_button = pygame.transform.scale(green_music_button, (size_music_button, size_music_button))

red_music_button = pygame.image.load("Assets/Music/Red Music Button.png")
red_music_button = pygame.transform.scale(red_music_button, (size_music_button, size_music_button))

image_music_button = green_music_button
coordinate_music_button = (screen_width - size_music_button + 20, screen_height - size_music_button + 20)
music_button_rect = green_music_button.get_rect(topleft=coordinate_music_button)

# For Level Map
background_image_level_map = pygame.image.load("Assets/Switch_Level/background.jpg").convert()
background_level_map = pygame.transform.scale(background_image_level_map, (screen_width // 2, screen_height))

all_planets_data = [{"image_path": "Assets/Switch_Level/planet1.png", "x": 650},
    {"image_path": "Assets/Switch_Level/planet2.png", "x": 1600},
    {"image_path": "Assets/Switch_Level/planet3.png", "x": 2250},
    {"image_path": "Assets/Switch_Level/planet4.png", "x": 2900}]
planets = []
planet_rects = []
for data in all_planets_data:
    planet_image = pygame.image.load(data["image_path"]).convert_alpha()
    planet = pygame.transform.scale(planet_image, (250, 250))
    planet_rect = planet.get_rect()
    planet_rect.x = data["x"]
    planet_rect.y = screen_height / 2 - 150
    planets.append(planet)
    planet_rects.append(planet_rect)

arrow_data = [{"image_path": "Assets/Switch_Level/left_arrow.png", "x": 75},
    {"image_path": "Assets/Switch_Level/right_arrow.png", "x": screen_width - 150}]
arrows = []
arrow_rects = []
for data in arrow_data:
    arrow_image = pygame.image.load(data["image_path"]).convert_alpha()
    arrow = pygame.transform.scale(arrow_image, (100, 80))
    arrow_rect = arrow.get_rect()
    arrow_rect.x = data["x"]
    arrow_rect.y = screen_height / 2 - 60
    arrows.append(arrow)
    arrow_rects.append(arrow_rect)

fps = 120  # Set FPS rate for frame rate

# Initialize TrajectorySimulation instance
trajectory_simulation = TrajectorySimulation(5, screen, screen_width, screen_height,background_image)
orbital_phase = OrbitalPhase(5, screen)

clock = pygame.time.Clock()
level_attempts = 0
circle_x = 864
circle_y = 0
time_step = 0
v = 100
alpha = 45
g = 9.81
h = 0

angle = 0
radius = 390

mouse_held = False
mouse_pressed = False
shooting_trajectory = False
orbital_game_phase = False
music_playing = True
menu = True
loaded_level=False

# Initialize the slider
slider = Slider((50, 50), 200, 0, 100, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_held = True

            if event.button == 1 and not music_button_rect.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                position_initial_x, position_initial_y = pygame.mouse.get_pos()

            if event.button == 3:
                # Cancel aiming when right mouse button is pressed
                mouse_pressed = False

            if music_button_rect.collidepoint(pygame.mouse.get_pos()):
                if image_music_button == red_music_button:
                    image_music_button = green_music_button
                    pygame.mixer.music.unpause()
                else:
                    image_music_button = red_music_button
                    pygame.mixer.music.pause()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False

            if loaded_level:
                if event.button == 1 and mouse_pressed:
                    shooting_trajectory = True

            if slider.dragging:  # Check if slider is being dragged
                slider.dragging = False  # Stop dragging when left mouse button is released

            if menu and button_rect.collidepoint(event.pos):  # Check if menu is active and button is clicked
                menu = False  # Set menu to False on click

        elif event.type == pygame.MOUSEMOTION:
            if slider.dragging:  # Check if slider is being dragged
                slider.update_value(event.pos)  # Update slider value based on mouse position

    # Main game loop
    screen.fill((0, 0, 0))
    time_step += clock.tick(fps) / 180

    # Get the mouse x and y
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_held:
        cursor = pygame.transform.scale(pygame.image.load("Assets/Cursor/cursor_hold.png"), (32, 32))
    else:
        cursor = pygame.transform.scale(pygame.image.load("Assets/Cursor/cursor_still.png"), (32, 32))

    if menu:
        # Draw the button
        button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100)
        pygame.draw.rect(screen, (255, 255, 255), button_rect)

    else:
        if not orbital_game_phase and not loaded_level:
            loaded_level, chosen_level = level_selection(screen, background_level_map, planets, planet_rects, arrows,arrow_rects)
            level_attempts=0

        if loaded_level:
            angle = 0
            # Calculate v continuously while mouse button is pressed
            if mouse_pressed:
                deplacement_x = position_initial_x - mouse_x
                deplacement_y = position_initial_y - mouse_y

                # Calculate the vector from the ball to the mouse
                vector_mouse = math.sqrt((mouse_x - position_initial_x) ** 2 + (mouse_y - position_initial_y) ** 2)

                # Calculate the angle between the x-axis
                if vector_mouse != 0:
                    alpha = math.degrees(math.acos(deplacement_x / vector_mouse))

                # Get a velocity from the mouse displacement
                v = 40 + deplacement_x / 10 - deplacement_y / 10

            # Projectile motion loop
            if shooting_trajectory:
                shooting_trajectory, orbital_game_phase, loaded_level,level_attempts = trajectory_simulation.projectile_motion(circle_x, circle_y, g, v, h, alpha, chosen_level, level_attempts, clock)
                if level_attempts > 2:
                    loaded_level=False
            else:
                trajectory_simulation.projectile_aim(g, v, h, alpha, time_step, chosen_level)

    if orbital_game_phase:
        # Increment angle for rotation
        angle -= 0.5
        # Draw and handle events for the slider
        slider.draw(screen)
        slider_value = slider.slider_value  # Get the current value of the slider

        # Draw the circle with updated angle
        orbital_game_phase = orbital_phase.draw_circle(radius, angle)

    # Display the music button
    screen.blit(image_music_button, coordinate_music_button)

    screen.blit(cursor, (mouse_x, mouse_y))
    pygame.display.flip()  # Update the display

pygame.quit()
