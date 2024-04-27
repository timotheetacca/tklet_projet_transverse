import pygame
import math
import random
from save import remove_life, add_level

screen_width, screen_height = 1536, 864


class OrbitalPhase:
    def __init__(self, circle_radius, screen, slider1, slider2, slider3):
        self.transparent_surface = pygame.Surface((1536, 864), pygame.SRCALPHA)
        self.circle_radius = circle_radius
        self.screen = screen
        self.angle = 0
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3
        self.font = pygame.font.Font("Assets/Font/pixela-extreme.ttf", 30)
        self.current_values = [50, 50, 50]
        self.current_color = [(255, 255, 255)] * 3

    def draw_circle(self, level_number, planet_scale, time_text):
        """
         Draw the circular motion of the rocket

         Parameters
         ----------
         level_number(int) : Level number
         planet_scale(int) : Scale of the planet image
         time_text(int) : Time to be displayed

         Returns
         -------
         bool : True if a full turn is made, False otherwise
         """
        # Get the center of the screen
        center_x, center_y = screen_width // 2, screen_height // 2

        # Calculate circle position
        x = center_x + self.circle_radius * math.cos(math.radians(self.angle))
        y = center_y + self.circle_radius * math.sin(math.radians(self.angle))

        # Load planet image based on level number
        planet_img = pygame.image.load(f"Assets/Level/Planets/planet{level_number}.png").convert_alpha()
        # Scale the planet image to the desired size
        planet_img = pygame.transform.scale(planet_img, (planet_scale, planet_scale))

        color_progress = time_text / 5000
        color = (int(255 * color_progress), int(255 * (1 - color_progress)), 0)

        time_text = self.font.render(f"{(time_text / 1000):.1f}s", True, color)
        self.screen.blit(time_text, (center_x - 25, (center_y + (planet_scale / 2) + 50)))

        # Blit the planet image onto the transparent surface
        self.screen.blit(planet_img, (center_x - (planet_scale / 2), center_y - (planet_scale / 2)))

        # Draw the circle
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 5)

        # Check if a full turn is made
        if self.angle <= -360:
            self.angle = 0
            add_level("game_save.txt")
            return False
        return True

    def update_angle(self, orbital_game_phase):
        """
        Update the angle of rotation for the orbit.

        Parameters
        ----------
        orbital_game_phase(bool) : Current phase of the orbital game

        Returns
        -------
        bool : True if the angle is updated, False if a full turn is made
        """
        self.angle -= 0.2

        if self.angle <= -360:
            self.angle = 0  # Reset the angle
            self.slider1.reset()
            self.slider2.reset()
            self.slider3.reset()
            self.current_color = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]
            self.current_values = [50, 50, 50]
            add_level("game_save.txt")
            return False
        return orbital_game_phase

    def check_timer(self, slider_value1, slider_value2, slider_value3, value_change_timer, value_check_timer,
                    orbital_game_phase):
        """
        Check timers and slider values to control the game state

        Parameters
        ----------
        slider_value1(int) : Value of slider 1
        slider_value2(int) : Value of slider 2
        slider_value3(int) : Value of slider 3
        value_change_timer(int) : Timer for changing values
        value_check_timer(int) : Timer for checking values
        orbital_game_phase(bool) : Current phase of the orbital game

        Returns
        -------
        bool: Updated game phase
        int : Change timer
        int : Value check timer
        """
        if value_change_timer >= 5000:
            # Change one of the values to match randomly
            index_to_change = random.randint(0, 2)
            self.current_values[index_to_change] = random.randint(0, 100)
            self.current_color = [(255, 255, 255)] * 3
            self.current_color[index_to_change] = (165, 0, 0)
            return True, 0, value_check_timer

        if value_check_timer >= 4950:
            # Compare slider values to current values
            if not (abs(slider_value1 - self.current_values[0]) <= 20 and
                    abs(slider_value2 - self.current_values[1]) <= 20 and
                    abs(slider_value3 - self.current_values[2]) <= 20):
                # if values don't match, close the level and lose a life
                self.current_color = [(255, 255, 255)] * 3
                self.current_values = [50, 50, 50]
                self.slider1.reset()
                self.slider2.reset()
                self.slider3.reset()
                self.angle = 0  # Reset the angle
                remove_life("game_save.txt")
                return False, 0, 0

            # Reset the timer after checking slider values
            return orbital_game_phase, value_change_timer, 0

        return orbital_game_phase, value_change_timer, value_check_timer

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
