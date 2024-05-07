import pygame.mixer
import math
from trajectory_simulation import TrajectorySimulation
from orbital_phase import OrbitalPhase

from slider import Slider
from save import update_save_information, add_level, update_lives, remove_life, display_life, update_level
from level_map import level_selection
from level import level
from scenario import display_text_scenario

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
background_space_sliders = pygame.image.load("Assets/Level/orbital_sliders.png")
background_space_sliders_advice = pygame.image.load("Assets/Level/orbital_values_advice.png")
background_space_orbital = pygame.image.load("Assets/Level/background_space_orbital.png")

# For Menu
menu_background_image = pygame.image.load("Assets/Menu/menu_background.png")
menu_background = pygame.transform.scale(menu_background_image, (screen_width, screen_height))

logo_image = pygame.image.load("Assets/Menu/tklet_logo.png")
logo = pygame.transform.scale(logo_image, (596.25, 215.25))
logo_rect = logo.get_rect()
logo_rect.x = screen_width // 2 - 300
logo_rect.y = screen_height // 2 - 150

illus_pic = pygame.image.load("Assets/Menu/illustration.png")
illus = pygame.transform.scale(illus_pic, (450, 450))
illus_rect = illus.get_rect()
illus_rect.x = screen_width // 2 - 225
illus_rect.y = screen_height // 2 - 425

play_button_image = pygame.image.load("Assets/Menu/play_button.png")
play_button = pygame.transform.scale(play_button_image, (225, 100))
play_button_rect = play_button.get_rect()
play_button_rect.x = screen_width // 2 - 100
play_button_rect.y = screen_height // 2 + 100

# For parameters
size_button = 75

Blue_QUIT_button_image = pygame.image.load("Assets/blue_quit.png")
Blue_QUIT_button = pygame.transform.scale(Blue_QUIT_button_image, (size_button, size_button))
coordinate_Blue_QUIT_button = (screen_width - size_button - 20, screen_height - size_button - 20)
Blue_QUIT_button_rect = Blue_QUIT_button.get_rect(topleft=coordinate_Blue_QUIT_button)
Red_QUIT_button_image = pygame.image.load("Assets/Game_over/red_quit.png")
Red_QUIT_button = pygame.transform.scale(Red_QUIT_button_image, (size_button, size_button))
coordinate_Red_QUIT_button = coordinate_Blue_QUIT_button
Red_QUIT_button_rect = Blue_QUIT_button_rect

ON_music_button = pygame.image.load("Assets/Music/ON Music Button.png")
ON_music_button = pygame.transform.scale(ON_music_button, (size_button, size_button))

OFF_music_button = pygame.image.load("Assets/Music/OFF Music Button.png")
OFF_music_button = pygame.transform.scale(OFF_music_button, (size_button, size_button))

image_music_button = ON_music_button
coordinate_music_button = (coordinate_Blue_QUIT_button[0] - 95, coordinate_Blue_QUIT_button[1])
music_button_rect = ON_music_button.get_rect(topleft=coordinate_music_button)

return_button_image = pygame.image.load("Assets/return.png")
return_button = pygame.transform.scale(return_button_image, (size_button, size_button))
coordinate_return_button = (coordinate_music_button[0] - 95, coordinate_Blue_QUIT_button[1])
return_button_rect = return_button.get_rect(topleft=coordinate_return_button)

# For Game over
game_over_title_image = pygame.image.load("Assets/Game_over/game_over.png")
game_over_title = pygame.transform.scale(game_over_title_image, (1092.8, 136))
game_over_title_rect = logo.get_rect()
game_over_title_rect.x = screen_width // 2 - 1092.8 / 2
game_over_title_rect.y = screen_height // 3 + 100

restart_button_image = pygame.image.load("Assets/Game_over/restart.png")
restart_button = pygame.transform.scale(restart_button_image, (225, 100))
restart_button_rect = play_button.get_rect()
restart_button_rect.x = screen_width // 2 - 100
restart_button_rect.y = screen_height // 2 + 150

rocket_explosion_image = pygame.image.load("Assets/Game_over/explosion.png")
rocket_explosion = pygame.transform.scale(rocket_explosion_image, (500, 500))
rocket_explosion_rect = logo.get_rect()
rocket_explosion_rect.x = screen_width // 2 - 500 / 2
rocket_explosion_rect.y = screen_height // 3 - 250

# For Level Map
background_image_level_map = pygame.image.load("Assets/Switch_Level/background.jpg").convert()
background_level_map = pygame.transform.scale(background_image_level_map, (screen_width // 2, screen_height))

all_planets_data = [{"image_path": "Assets/Level/Planets/planet1.png", "x": 650},
                    {"image_path": "Assets/Level/Planets/planet2.png", "x": 1350},
                    {"image_path": "Assets/Level/Planets/planet3.png", "x": 2050},
                    {"image_path": "Assets/Level/Planets/planet4.png", "x": 2750},
                    {"image_path": "Assets/Level/Planets/planet5.png", "x": 3450},
                    {"image_path": "Assets/Level/Planets/planet6.png", "x": 4150}]
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
                           {"image_path": "Assets/Switch_Level/planet4_locked.png", "x": 2750},
                           {"image_path": "Assets/Switch_Level/planet5_locked.png", "x": 3450},
                           {"image_path": "Assets/Switch_Level/planet6_locked.png", "x": 4150}]
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

# For Sound Design
level_lose_sound = pygame.mixer.Sound("Assets/Music/level_lose.mp3")
play_sound = pygame.mixer.Sound("Assets/Music/play_button.mp3")

fps = 120  # Set FPS rate for frame rate
delta_time = 0

# Initialize TrajectorySimulation instance
trajectory_simulation = TrajectorySimulation(5, screen, screen_width, screen_height, background_image)

clock = pygame.time.Clock()
level_attempts = 0
rocket_x = 864
rocket_y = 0
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
object_state = False
music_loaded = False
loaded_level = False
tutorial_game_phase_done = False

# Initialize the sliders with initial values set to 50
slider1 = Slider((50, 200), 200, 0, 100, 50)
slider2 = Slider((50, 400), 200, 0, 100, 50)
slider3 = Slider((50, 600), 200, 0, 100, 50)

# Initialize variables for value change timer and current values
value_change_timer_orbital = 0
current_values_orbital = [50, 50, 50]
current_color_orbital = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]

orbital_phase = OrbitalPhase(390, screen, slider1, slider2, slider3)
chosen_level = -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
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

            if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.music.unpause()
                update_lives("game_save.txt", 3)
                if last_level != 1:
                    update_level("game_save.txt", last_level - 1)
                player_save = update_save_information("game_save.txt")

            elif Red_QUIT_button_rect.collidepoint(pygame.mouse.get_pos()):
                update_lives("game_save.txt", 3)
                if last_level != 1:
                    update_level("game_save.txt", last_level - 1)
                player_save = update_save_information("game_save.txt")
                pygame.mixer.music.stop()
                pygame.quit()

            if Blue_QUIT_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.music.stop()
                pygame.quit()

            if music_button_rect.collidepoint(pygame.mouse.get_pos()):
                if image_music_button == OFF_music_button:
                    image_music_button = ON_music_button
                    pygame.mixer.music.unpause()
                else:
                    image_music_button = OFF_music_button
                    pygame.mixer.music.pause()

            if return_button_rect.collidepoint(pygame.mouse.get_pos()):
                if loaded_level:
                    loaded_level=False
                else:
                    menu=True
                    
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

            if menu and play_button_rect.collidepoint(event.pos):  # Check if menu is active and button is clicked
                play_sound.play()
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
        screen.blit(menu_background, (0, 0))
        screen.blit(Blue_QUIT_button, coordinate_Blue_QUIT_button)
        screen.blit(play_button, play_button_rect)
        screen.blit(illus, illus_rect)
        screen.blit(logo, logo_rect)
        player_save = update_save_information("game_save.txt")
        last_level = player_save[0]
        scenario = (last_level == 0)

    else:

        if scenario:
            add_level("game_save.txt")
            level(level_number=0, screen=screen, transparent_surface=None, time_step=None, rocket_x=None, rocket_y=None,
                  object_state=None)
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

            screen.blit(return_button, coordinate_return_button)
            screen.blit(image_music_button, coordinate_music_button)

        if player_save[1] == 0:
            pygame.mixer.music.pause()
            screen.fill((0, 0, 0))
            screen.blit(rocket_explosion, rocket_explosion_rect)
            screen.blit(game_over_title, game_over_title_rect)
            screen.blit(restart_button, restart_button_rect)
            screen.blit(Red_QUIT_button, coordinate_Red_QUIT_button)

        if loaded_level:
            angle = 0
            # Calculate v continuously while mouse button is pressed
            if mouse_held and mouse_pressed:
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
                shooting_trajectory, orbital_game_phase, loaded_level, level_attempts, object_state = trajectory_simulation.projectile_motion(
                    rocket_x, rocket_y, g, v, h, alpha, chosen_level, level_attempts, clock, object_state)
                if level_attempts > 2:
                    loaded_level = False
                    object_state = False
                    remove_life("game_save.txt")
                    level_lose_sound.play()

            else:
                # Display the aim trajectory on the screen
                trajectory_simulation.projectile_aim(g, v, h, alpha, time_step, chosen_level, level_attempts,
                                                     object_state)
            if level_attempts<2:
                screen.blit(return_button, coordinate_return_button)
            screen.blit(image_music_button, coordinate_music_button)

    if not tutorial_game_phase_done and orbital_game_phase:
        text_phase1_tutorial_phase = """Oh, you’ve managed to enter this planet’s orbit! Now you have to 
        calibrate your rocket ship in order to achieve a state of orbital stationement! The goal is to make a 
        full turn around the planet! Use your engineering skills to re-evaluate your rocket's parameters!"""

        display_text_scenario(text_phase1_tutorial_phase, background_image, skip_allowed=False, fade_out=False)

        text_phase2_tutorial_phase = """See the cursors to your left?"""
        display_text_scenario(text_phase2_tutorial_phase, background_space_sliders, skip_allowed=False,
                              fade_out=False)

        text_phase3_tutorial_phase = """Try to match their values with the values on your right! But be careful, 
        you only have 5 seconds between each re-evaluation! I'll start a stopwatch as soon as you enter orbit, 
        but don't panic, I'll leave you alone for the first 5 seconds! Good luck!"""

        display_text_scenario(text_phase3_tutorial_phase, background_space_sliders_advice, skip_allowed=False,
                              fade_out=False)

        tutorial_game_phase_done = True

    if orbital_game_phase and tutorial_game_phase_done:
        screen.blit(background_space_orbital, (0, 0))

        # Draw and handle events for the slider
        slider1.draw(screen)
        slider_value1 = slider1.slider_value  # Get the current value of the slider

        slider2.draw(screen)
        slider_value2 = slider2.slider_value

        slider3.draw(screen)
        slider_value3 = slider3.slider_value

        # Draw the circle with updated angle
        orbital_game_phase = orbital_phase.draw_circle(chosen_level, 350)

        orbital_phase.display_values()

        # Increment and check angle for rotation
        orbital_game_phase = orbital_phase.update_angle(orbital_game_phase, delta_time)
        orbital_game_phase = orbital_phase.check_timer(slider_value1, slider_value2, slider_value3, orbital_game_phase,
                                                       level_lose_sound)
        delta_time = clock.tick(fps) / 1000
        screen.blit(image_music_button, coordinate_music_button)

    if player_save[1] != 0:
        # Display the quit button
        screen.blit(Blue_QUIT_button, coordinate_Blue_QUIT_button)

    screen.blit(cursor, (mouse_x, mouse_y))
    pygame.display.flip()  # Update the display
