import pygame
import math
import random
from save import remove_life, add_level

screen_width, screen_height = 1536, 864
win_sound = pygame.mixer.Sound("Assets/Music/level_win.mp3")


class OrbitalPhase:
    def __init__(self, circle_radius, screen, slider1, slider2, slider3):
        self.start_time = None
        self.transparent_surface = pygame.Surface((1536, 864), pygame.SRCALPHA)
        self.circle_radius = circle_radius
        self.screen = screen
        self.angle = 0
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3
        self.elapsed_time = 0
        self.font = pygame.font.Font("Assets/Font/pixela-extreme.ttf", 30)
        self.current_values = [50, 50, 50]
        self.current_color = [(255, 255, 255)] * 3

    def draw_circle(self, level_number, planet_scale):
        """
        Draw the circular motion of the rocket

        Parameters
        ----------
        level_number(int) : Level number
        planet_scale(int) : Scale of the planet image

        Returns
        -------
        bool : True if a full turn is made, False otherwise
        """
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()

        # Get the center of the screen
        center_x, center_y = screen_width // 2, screen_height // 2

        # Calculate circle position
        x = center_x + self.circle_radius * math.cos(math.radians(self.angle))
        y = center_y + self.circle_radius * math.sin(math.radians(self.angle))

        # Load planet image based on level number
        planet_img = pygame.image.load(f"Assets/Level/Planets/planet{level_number}.png").convert_alpha()
        # Scale the planet image to the desired size
        planet_img = pygame.transform.scale(planet_img, (planet_scale, planet_scale))

        # Calculate time elapsed
        current_time = pygame.time.get_ticks()
        self.elapsed_time = current_time - self.start_time

        # Calculate the color in function of time left
        color_progress = self.elapsed_time / 5000
        color = (int(255 * color_progress), int(255 * (1 - color_progress)), 0)

        # Display time
        time_text = self.font.render(f"{(self.elapsed_time / 1000):.1f}s", True, color)
        self.screen.blit(time_text, (center_x - 25, (center_y + (planet_scale / 2) + 50)))

        # Blit the planet image onto the transparent surface
        self.screen.blit(planet_img, (center_x - (planet_scale / 2), center_y - (planet_scale / 2)))

        rocket_image = pygame.image.load('Assets/rocket.png')
        rocket_image = pygame.transform.scale(rocket_image, (44, 30))

        # Rotate the rocket image based on the trajectory angle
        rotated_rocket = pygame.transform.rotate(rocket_image, -self.angle+90)
        rocket_rect = rotated_rocket.get_rect(center=(x,y))

        self.screen.blit(rotated_rocket, rocket_rect)
        return True

    def update_angle(self, orbital_game_phase, delta_time):
        """
        Update the angle of rotation for the orbit.

        Parameters
        ----------
        orbital_game_phase(bool) : Current phase of the orbital game
        delta_time(int) : Time elapsed since last frame in seconds

        Returns
        -------
        bool : True if the angle is updated, False if a full turn is made
        """
        angle_increment_per_second = 20  # Angle increase per second
        angle_increment = angle_increment_per_second * delta_time

        self.angle -= angle_increment

        if self.angle <= -360:
            self.angle = 0  # Reset the angle
            self.slider1.reset()
            self.slider2.reset()
            self.slider3.reset()
            self.current_color = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]
            self.current_values = [50, 50, 50]
            self.start_time = None
            self.elapsed_time = 0
            add_level("game_save.txt")
            win_sound.play()
            return False

        return orbital_game_phase

    def check_timer(self, slider_value1, slider_value2, slider_value3, orbital_game_phase, lose_sound):
        """
        Check timers and slider values to control the game state

        Parameters
        ----------
        slider_value1(int) : Value of slider 1
        slider_value2(int) : Value of slider 2
        slider_value3(int) : Value of slider 3
        orbital_game_phase(bool) : Current phase of the orbital game

        Returns
        -------
        bool: Updated game phase
        int : Change timer
        int : Value check timer
        """
        if self.elapsed_time >= 5000:
            # Change one of the values to match randomly
            index_to_change = random.randint(0, 2)
            self.current_values[index_to_change] = random.randint(0, 100)
            self.current_color = [(255, 255, 255)] * 3
            self.current_color[index_to_change] = (165, 0, 0)
            self.start_time = None
            self.elapsed_time = 0
            return True

        if self.elapsed_time >= 4950:
            # Compare slider values to current values
            sound = pygame.mixer.Sound("Assets/Music/validation_orbital.mp3")
            sound.set_volume(0.5)
            sound.play()
            if not (abs(slider_value1 - self.current_values[0]) <= 10 and
                    abs(slider_value2 - self.current_values[1]) <= 10 and
                    abs(slider_value3 - self.current_values[2]) <= 10):
                # if values don't match, close the level and lose a life
                self.current_color = [(255, 255, 255)] * 3
                self.current_values = [50, 50, 50]
                self.slider1.reset()
                self.slider2.reset()
                self.slider3.reset()
                self.start_time = None
                self.elapsed_time = 0
                self.angle = 0  # Reset the angle
                remove_life("game_save.txt")
                lose_sound.play()
                return False

            # Reset the timer after checking slider values
            return orbital_game_phase
        return orbital_game_phase

    def display_values(self):
        """
        Display the values that the user should match on the screen

        Parameters
        -------
        None

        Returns
        -------
        None
        """
        # Display the values that the user should match on the right side of the screen
        font = pygame.font.Font("Assets/Font/pixela-extreme.ttf", 36)
        text_value1 = font.render(str(self.current_values[0]), True, self.current_color[0])
        text_value2 = font.render(str(self.current_values[1]), True, self.current_color[1])
        text_value3 = font.render(str(self.current_values[2]), True, self.current_color[2])
        self.screen.blit(text_value1, (1300, 200))
        self.screen.blit(text_value2, (1300, 400))
        self.screen.blit(text_value3, (1300, 600))
