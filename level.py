import pygame

screen_width, screen_height = 1536, 864


def planet(transparent_surface, position, planet_radius, orbit_radius, level_number):
    # Create a surface with the desired transparency
    pygame.draw.circle(transparent_surface, (255, 255, 255, 100), (position[0], position[1]), orbit_radius)

    # Load planet image based on level number
    planet_img = pygame.image.load(f"Assets/Level/Planets/planet{level_number}.png").convert_alpha()

    # Scale the planet image to the desired size
    planet_img = pygame.transform.scale(planet_img, (planet_radius * 2, planet_radius * 2))

    # Blit the planet image onto the transparent surface
    transparent_surface.blit(planet_img, (position[0] - planet_radius, position[1] - planet_radius))


def level(level_number, screen, transparent_surface):
    if level_number == 1:
        planet_radius = 45
        orbit_radius = 130
        position = (900, 425)
        screen.blit(transparent_surface, (0, 0))
        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)

        return orbit_radius, position, [], []

    if level_number == 2:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)
        screen.blit(transparent_surface, (0, 0))
        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)

        # Add all the obstacles contained in the level
        obstacles = [pygame.Rect(700, 460, 40, 40), pygame.Rect(700, 250, 40, 40)]

        return orbit_radius, position, obstacles, []

    if level_number == 3:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 250)
        screen.blit(transparent_surface, (0, 0))
        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)

        # Add all the obstacles contained in the level
        obstacles = [pygame.Rect(700, 350, 40, 40), pygame.Rect(700, 410, 40, 40), pygame.Rect(760, 470, 40, 40),
                     pygame.Rect(850, 260, 40, 40)]

        # Add all the objects contained in the level
        objects = [["shield",pygame.Rect(500, 500, 30, 30)]]

        return orbit_radius, position, obstacles, objects

    if level_number == 4:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)

        # Add all the obstacles contained in the level
        obstacles = []

        # Add all the objects contained in the level
        objects = []

        return orbit_radius, position, obstacles, objects
