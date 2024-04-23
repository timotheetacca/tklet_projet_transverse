import pygame.mixer
import math
import random
from trajectory_simulation import TrajectorySimulation
from orbital_phase import OrbitalPhase

from slider import Slider
from save import update_save_information, add_level, remove_life, display_life
from level_map import level_selection
from level import level

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

all_planets_data = [{"image_path": "Assets/Level/Planets/planet1.png", "x": 650},
                    {"image_path": "Assets/Level/Planets/planet2.png", "x": 1350},
                    {"image_path": "Assets/Level/Planets/planet3.png", "x": 2050},
                    {"image_path": "Assets/Level/Planets/planet4.png", "x": 2750}]
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

all_locked_planets_data = [{"image_path": "Assets/Switch_Level/planet2_locked.png", "x": 1350},
                           {"image_path": "Assets/Switch_Level/planet3_locked.png", "x": 2050},
                           {"image_path": "Assets/Switch_Level/planet4_locked.png", "x": 2750}]
locked_planets = []
locked_planet_rects = []
for data in all_locked_planets_data:
    locked_planet_image = pygame.image.load(data["image_path"]).convert_alpha()
    locked_planet = pygame.transform.scale(locked_planet_image, (250, 250))
    locked_planet_rect = locked_planet.get_rect()
    locked_planet_rect.x = data["x"]
    locked_planet_rect.y = screen_height / 2 - 150
    locked_planets.append(locked_planet)
    locked_planet_rects.append(locked_planet_rect)

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
trajectory_simulation = TrajectorySimulation(5, screen, screen_width, screen_height, background_image)
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
music_playing = False
scenario = True
menu = True
music_loaded = False
loaded_level = False

# Initialize the sliders with initial values set to 50
slider1 = Slider((50, 200), 200, 0, 100, 50)
slider2 = Slider((50, 400), 200, 0, 100, 50)
slider3 = Slider((50, 600), 200, 0, 100, 50)

# Initialize variables for value change timer and current values
value_change_timer_orbital = 0
current_values_orbital = [50, 50, 50]
current_color_orbital =[(255, 255, 255),(255, 255, 255),(255, 255, 255)]

# Initialize timer for value check
value_check_timer = 0
value_change_timer = 0

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

            # Handle the 3 sliders
            if slider1.is_over_handle(event.pos):
                slider1.dragging = True

            if slider2.is_over_handle(event.pos):
                slider2.dragging = True

            if slider3.is_over_handle(event.pos):
                slider3.dragging = True

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
                    mouse_pressed = False
                    shooting_trajectory = True

            if slider1.dragging:  # Check if slider is being dragged
                slider1.dragging = False  # Stop dragging when left mouse button is released

            if slider2.dragging:
                slider2.dragging = False

            if slider3.dragging:
                slider3.dragging = False

            if menu and button_rect.collidepoint(event.pos):  # Check if menu is active and button is clicked
                menu = False  # Set menu to False on click

        elif event.type == pygame.MOUSEMOTION:
            if slider1.dragging:  # Check if slider is being dragged
                slider1.update_value(event.pos)  # Update slider value based on mouse position

            if slider2.dragging:  #
                slider2.update_value(event.pos)

            if slider3.dragging:
                slider3.update_value(event.pos)

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
        player_save = update_save_information("game_save.txt")
        last_level = player_save[0]
        scenario = (last_level == 0)

    else:

        if scenario:
            add_level("game_save.txt")
            level(level_number=0, screen=screen, transparent_surface=None, time_step=None)
            scenario = False

        if not music_playing:
            pygame.mixer.music.load("Assets/Music/musicTKLET-Game.mp3")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
            music_playing = True

        if not orbital_game_phase and not loaded_level:
            chosen_level = level_selection(screen, background_level_map, planets, planet_rects, locked_planets,
                                           locked_planet_rects, arrows, arrow_rects, last_level)
            player_save = update_save_information("game_save.txt")
            last_level = player_save[0]
            display_life(player_save[1], screen, "Assets/heart_image.png")

            if chosen_level != 0 and chosen_level <= last_level:
                loaded_level = True
                level_attempts = 0

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
                shooting_trajectory, orbital_game_phase, loaded_level, level_attempts = trajectory_simulation.projectile_motion(
                    circle_x, circle_y, g, v, h, alpha, chosen_level, level_attempts, clock)
                if level_attempts > 2:
                    loaded_level = False
                    remove_life("game_save.txt")
            else:
                trajectory_simulation.projectile_aim(g, v, h, alpha, time_step, chosen_level, level_attempts)

    if orbital_game_phase:
        background_space_orbital = pygame.image.load("Assets/Level/background_space_orbital.png")
        screen.blit(background_space_orbital, (0, 0))

        # Increment angle for rotation
        angle -= 0.2

        # Draw and handle events for the slider
        slider1.draw(screen)
        slider_value1 = slider1.slider_value  # Get the current value of the slider

        slider2.draw(screen)
        slider_value2 = slider2.slider_value

        slider3.draw(screen)
        slider_value3 = slider3.slider_value

        # Draw the circle with updated angle
        orbital_game_phase = orbital_phase.draw_circle(radius, angle)

        # Check if it's time to change one of the values to match
        if value_change_timer >= 4000:
            # Change one of the values to match randomly
            index_to_change = random.randint(0, 2)
            current_values_orbital[index_to_change] = random.randint(0, 100)
            current_color_orbital = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]
            current_color_orbital[index_to_change] = (139,0,0)
            # Reset the timer
            value_change_timer = 0

        # Display the values that the user should match on the right side of the screen
        font = pygame.font.Font(None, 36)
        text_value1 = font.render(str(current_values_orbital[0]), True, current_color_orbital[0])
        text_value2 = font.render(str(current_values_orbital[1]), True, current_color_orbital[1])
        text_value3 = font.render(str(current_values_orbital[2]), True, current_color_orbital[2])

        screen.blit(text_value1, (1300, 200))
        screen.blit(text_value2, (1300, 400))
        screen.blit(text_value3, (1300, 600))

        # Check if it's time to verify the slider values after 8 seconds
        if value_check_timer >= 8000:
            # Compare slider values to current values
            if not (abs(slider_value1 - current_values_orbital[0]) <= 20 and
                    abs(slider_value2 - current_values_orbital[1]) <= 20 and
                    abs(slider_value3 - current_values_orbital[2]) <= 20):

                # if values don't match, close the level and lose a life
                print(abs(slider_value1 - current_values_orbital[0]))
                print(abs(slider_value2 - current_values_orbital[1]))
                print(abs(slider_value3 - current_values_orbital[2]))
                current_values_orbital = [50, 50, 50]
                slider1.reset()
                slider2.reset()
                slider3.reset()
                orbital_game_phase = False
                remove_life("game_save.txt")

            # Reset the timer after checking slider values
            value_check_timer = 0
        else:
            # Increment the timer
            value_check_timer += clock.get_time()

        # Increment the timer for value change
        value_change_timer += clock.get_time()

    # Display the music button
    screen.blit(image_music_button, coordinate_music_button)

    screen.blit(cursor, (mouse_x, mouse_y))
    pygame.display.flip()  # Update the display
