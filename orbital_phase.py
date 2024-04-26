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
        # Get the center of the screen
        center_x, center_y = screen_width // 2, screen_height // 2

        # Calculate circle position
        x = center_x + self.circle_radius * math.cos(math.radians(self.angle))
        y = center_y + self.circle_radius * math.sin(math.radians(self.angle))

        # Load planet image based on level number
        planet_img = pygame.image.load(f"Assets/Level/Planets/planet{level_number}.png").convert_alpha()
        # Scale the planet image to the desired size
        planet_img = pygame.transform.scale(planet_img, (planet_scale, planet_scale))

        time_text = self.font.render(f"{(time_text / 1000):.1f}s", True, (255, 255, 255))
        self.screen.blit(time_text, (center_x-25, (center_y + (planet_scale / 2) + 50)))

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

    def update_angle(self):
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
        return True

    def check_timer(self, slider_value1, slider_value2, slider_value3, value_change_timer, value_check_timer):

        if value_change_timer >= 5000:
            # Change one of the values to match randomly
            index_to_change = random.randint(0, 2)
            self.current_values[index_to_change] = random.randint(0, 100)
            self.current_color = [(255, 255, 255)] * 3
            self.current_color[index_to_change] = (139, 0, 0)
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
            return True, value_change_timer, 0

        return True, value_change_timer, value_check_timer

    def display_values(self):
        # Display the values that the user should match on the right side of the screen
        font = pygame.font.Font("Assets/Font/pixela-extreme.ttf", 36)
        text_value1 = font.render(str(self.current_values[0]), True, self.current_color[0])
        text_value2 = font.render(str(self.current_values[1]), True, self.current_color[1])
        text_value3 = font.render(str(self.current_values[2]), True, self.current_color[2])
        self.screen.blit(text_value1, (1300, 200))
        self.screen.blit(text_value2, (1300, 400))
        self.screen.blit(text_value3, (1300, 600))
