import pygame.mixer
import math
from trajectory_simulation import TrajectorySimulation
from orbital_phase import OrbitalPhase
from slider import Slider  # Assuming Slider class is defined in slider.py
from level import level

pygame.init()
pygame.mixer.init()

# Set up the window
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Efreispace")

cursor_image = pygame.image.load("Assets/Cursor/cursor_still.png")
cursor = pygame.transform.scale(cursor_image, (32, 32))
pygame.mouse.set_visible(False)

# Music parameters

pygame.mixer.music.load("Assets/Music/musicTKLET-Game.mp3")
pygame.mixer.music.set_volume(0.25)


size_music_button = 90
green_music_button = pygame.image.load("Assets/Music/Green Music Button.png")
green_music_button = pygame.transform.scale(green_music_button, (size_music_button, size_music_button))

red_music_button = pygame.image.load("Assets/Music/Red Music Button.png")
red_music_button = pygame.transform.scale(red_music_button, (size_music_button, size_music_button))

image_music_button = green_music_button
coordinate_music_button = (screen_width - size_music_button + 20, screen_height - size_music_button + 20)
music_button_rect = green_music_button.get_rect(topleft=coordinate_music_button)

fps = 120  # Set FPS rate for frame rate

# Initialize TrajectorySimulation instance
trajectory_simulation = TrajectorySimulation(5, screen, screen_width, screen_height)
orbital_phase = OrbitalPhase(5, screen)

level_number = 1
circle_x = 864
circle_y = 0
time_step = 0
v = 100
alpha = 45
g = 9.81
h = 0

angle = 0
radius = 390

mouse_pressed = False
shooting_trajectory = False
stop_level = False
orbital_game_phase = False
music_playing = False
scenario = True
menu = True

# Initialize the slider
slider = Slider((50, 50), 200, 0, 100, 50)  # Example position, width, min_value, max_value, and initial_value

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cursor_image = pygame.image.load("Assets/Cursor/cursor_hold.png")
                cursor = pygame.transform.scale(cursor_image, (32, 32))

                left_click_pos = event.pos

                if not music_button_rect.collidepoint(left_click_pos):

                    if orbital_game_phase is False:
                        mouse_pressed = True
                        position_initiale_x, position_initiale_y = pygame.mouse.get_pos()

                    if menu:
                        # Check if mouse click is inside the rectangle
                        if button_rect.collidepoint(event.pos):
                            menu = False  # Set menu to False on click

                else:
                    if music_button_rect.collidepoint(pygame.mouse.get_pos()):

                        if image_music_button == red_music_button:

                            image_music_button = green_music_button
                            pygame.mixer.music.unpause()

                        else:

                            image_music_button = red_music_button
                            pygame.mixer.music.pause()

                if menu:
                    # Check if mouse click is inside the rectangle
                    if button_rect.collidepoint(event.pos):
                        menu = False  # Set menu to False on click

                    if slider.is_over_handle(event.pos):
                        slider.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                cursor_image = pygame.image.load("Assets/Cursor/cursor_still.png")
                cursor = pygame.transform.scale(cursor_image, (32, 32))

            if not music_button_rect.collidepoint(left_click_pos):
                if orbital_game_phase is False:
                    mouse_pressed = False
                    shooting_trajectory = True
                    stop_level = False

                if menu:
                    slider.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if slider.dragging:  # Check if slider is being dragged
                slider.update_value(event.pos)  # Update slider value based on mouse position

    screen.fill((0, 0, 0))

    # Get the mouse x and y
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if menu:
        # Draw the button
        button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100)
        pygame.draw.rect(screen, (255, 255, 255), button_rect)

        # Draw and handle events for the slider
        slider.draw(screen)
        slider_value = slider.slider_value  # Get the current value of the slider
        # print("Slider 1:", slider_value)  # Print slider value to console

    else:

        if scenario:
            level(level_number=-1, screen=screen, transparent_surface=None)
            scenario = False

        if not music_playing:
            pygame.mixer.music.play(-1)
            music_playing = True

        if orbital_game_phase is False:
            angle = 0

            # Calculate v continuously while mouse button is pressed
            if mouse_pressed:
                deplacement_x = position_initiale_x - mouse_x
                deplacement_y = position_initiale_y - mouse_y

                # Calculate the vector from the ball to the mouse
                vector_mouse = math.sqrt((mouse_x - position_initiale_x) ** 2 + (mouse_y - position_initiale_y) ** 2)

                # Calculate the angle between the x-axis
                if vector_mouse != 0:
                    alpha = math.degrees(math.acos(deplacement_x / vector_mouse))

                # Get a velocity from the mouse displacement
                v = 40 + deplacement_x / 10 - deplacement_y / 10

            # Projectile motion loop
            if shooting_trajectory:

                shooting_trajectory, level_number, orbital_game_phase = trajectory_simulation.projectile_motion(
                    circle_x, circle_y, g, v, h, alpha, level_number)

            else:
                trajectory_simulation.projectile_aim(g, v, h, alpha, time_step, level_number)

        else:
            # Increment angle for rotation
            angle -= 0.1

            # Draw the circle with updated angle
            orbital_game_phase = orbital_phase.draw_circle(radius, angle)

            orbital_phase.orbital_requirements()

    # Display the music button
    screen.blit(image_music_button, coordinate_music_button)

    screen.blit(cursor, (mouse_x, mouse_y))
    pygame.display.flip()  # Update the display

pygame.mixer.quit()
pygame.quit()
