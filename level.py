import pygame

screen_width, screen_height = 1536, 864

def animate_images(screen, list_images, size, position, current_image):
    animation_img = pygame.image.load(list_images[current_image]).convert_alpha()
    animation_img = pygame.transform.scale(animation_img, size)
    screen.blit(animation_img, position)

def current_frame(frame, list_images):
    return int((frame+1) % len(list_images))


def planet(transparent_surface, position, planet_radius, orbit_radius, level_number):
    # Create a surface with the desired transparency
    pygame.draw.circle(transparent_surface, (255, 255, 255, 100), (position[0], position[1]), orbit_radius)

    # Load planet image based on level number
    planet_img = pygame.image.load(f"Assets/Level/Planets/planet{level_number}.png").convert_alpha()

    # Scale the planet image to the desired size
    planet_img = pygame.transform.scale(planet_img, (planet_radius * 2, planet_radius * 2))

    # Blit the planet image onto the transparent surface
    transparent_surface.blit(planet_img, (position[0] - planet_radius, position[1] - planet_radius))


def level(level_number, screen, transparent_surface, time_step):
    if level_number == 1:
        planet_radius = 45
        orbit_radius = 130
        position = (900, 425)
        screen.blit(transparent_surface, (0, 0))
        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)

        frame_img = pygame.image.load("Assets/Level/Character/frame.png").convert_alpha()
        frame_img = pygame.transform.scale(frame_img, (342, 87))
        screen.blit(frame_img, (10, 10))

        character_paths = [
            "Assets/Level/Character/character_1.png",
            "Assets/Level/Character/character_2.png",
            "Assets/Level/Character/character_3.png"
        ]

        frame = current_frame(time_step, character_paths)

        animate_images(screen, character_paths, (60,60), (20,25), frame)

        font = (pygame.font.Font("Assets/pixel_art_font.ttf", 22))
        text = font.render("Drag your mouse backward to set ", True, (255, 255, 255))
        text2 = font.render("the angle and power of the shot,", True, (255, 255, 255))
        text3 = font.render("then releasing it to launch !", True, (255, 255, 255))
        screen.blit(text, (100,28))
        screen.blit(text2, (100, 45))
        screen.blit(text3, (100, 62))


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
        objects = [["shield", pygame.Rect(500, 500, 30, 30)]]

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
        objects = [["shield", pygame.Rect(500, 500, 30, 30)]]

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
