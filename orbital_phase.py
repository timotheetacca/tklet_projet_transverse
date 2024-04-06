import pygame
import math

pygame.init()

screen_width, screen_height = 1536, 864
class OrbitalPhase:
    def __init__(self,circle_radius, screen):
        self.transparent_surface = pygame.Surface((1536, 864), pygame.SRCALPHA)
        self.circle_radius = circle_radius
        self.screen = screen


    def draw_circle(self, radius, angle):

        # Get the center of the screen
        center_x, center_y = screen_width // 2, screen_height // 2

        # Calculate circle position
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))

        # Draw the circle
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 5)


        # Check if a full turn is made
        if angle <= -360:
            return False, 0

        return True, 0


