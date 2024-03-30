import pygame
from scenario import display_text_scenario

screen_width, screen_height = 1536, 864


def planet(screen, transparent_surface, position, planet_radius, orbit_radius):
    # Create a surface with the desired transparency
    transparent_surface_planet = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.circle(transparent_surface, (255, 255, 255, 100), (position[0], position[1]), orbit_radius)
    pygame.draw.circle(transparent_surface, (255, 255, 255, 250), (position[0], position[1]), planet_radius)


def level(level_number, screen, transparent_surface):
    if level_number == -1:

        screen.fill((0, 0, 0))
        pygame.display.flip()

        story = """The year is 2378. In a parallel universe called Nebulaëris, the Orion System shines like a beacon in the black immensity. It is an oasis of life in a sea of nebulae and dead stars. You are Kornus, a talented aerospace engineer. Your childhood best friend, Thorne, shares your passion for space exploration. You grew up together, dreaming of traveling to the stars and discovering the secrets of the universe. But one day, your dream turns into a nightmare. Thorne is abducted by aliens from the planet XFE-462, a mysterious planet located in the Orion System. Your world collapses around you. You can't imagine your life without Thorne. You are determined to save him, no matter the cost. Using your engineering skills, you build a revolutionary rocket capable of traveling from planet to planet. It's a crazy bet, a suicide mission, but you're willing to do anything to find your friend. Your journey will take you through the dangers of space.  But you will never give up hope. You know that Thorne is out there somewhere, waiting to be rescued."""

        display_text_scenario(story)

    if level_number == 1:
        planet_radius = 45
        orbit_radius = 130
        position = (900, 425)
        screen.blit(transparent_surface, (0, 0))
        planet(screen, transparent_surface, position, planet_radius, orbit_radius)

        obstacles = []

        return orbit_radius, position, obstacles

    if level_number == 2:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)
        screen.blit(transparent_surface, (0, 0))
        planet(screen, transparent_surface, position, planet_radius, orbit_radius)

        obstacles = []
        obstacle_rect = pygame.Rect(700, 460, 40, 40)
        obstacle_rect2 = pygame.Rect(700, 250, 40, 40)

        obstacles.append(obstacle_rect)
        obstacles.append(obstacle_rect2)

        return orbit_radius, position, obstacles

    if level_number == 3:
        planet_radius = 0
        orbit_radius = 0
        position = (0, 0)

        obstacles = []

        return orbit_radius, position, obstacles
