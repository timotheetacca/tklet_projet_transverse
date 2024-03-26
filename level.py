import pygame

screen_width, screen_height = 1536, 864


def planet(screen, transparent_surface, position, planet_radius, orbit_radius):
    # Create a surface with the desired transparency
    transparent_surface_planet = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.circle(transparent_surface, (255, 255, 255, 100), (position[0], position[1]), orbit_radius)
    pygame.draw.circle(transparent_surface, (255, 255, 255, 250), ((position[0], position[1])), planet_radius)


def level(level_number, screen, transparent_surface):
    if level_number == 1:
        planet_radius = 45
        orbit_radius = 130
        position = (900, 425)
        screen.blit(transparent_surface, (0, 0))
        planet(screen, transparent_surface, position, planet_radius, orbit_radius)

        return orbit_radius, position, [], []

    if level_number == 2:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)
        screen.blit(transparent_surface, (0, 0))
        planet(screen, transparent_surface, position, planet_radius, orbit_radius)

        # Add all the obstacles contained in the level
        obstacles = [pygame.Rect(700, 460, 40, 40), pygame.Rect(700, 250, 40, 40)]

        return orbit_radius, position, obstacles, []

    if level_number == 3:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)
        screen.blit(transparent_surface, (0, 0))
        planet(screen, transparent_surface, position, planet_radius, orbit_radius)

        # Add all the obstacles contained in the level
        obstacles = [pygame.Rect(700, 350, 40, 40), pygame.Rect(700, 450, 40, 40)]

        # Add all the objects contained in the level
        objects = [pygame.Rect(500, 460, 30, 30)]

        return orbit_radius, position, obstacles, objects
