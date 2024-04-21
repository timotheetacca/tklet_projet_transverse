import pygame
from scenario import display_text_scenario

screen_width, screen_height = 1536, 864

def animate_images(screen, list_images, size, position, current_image):
    # Animate an image using as a gif
    animation_img = pygame.image.load(list_images[current_image]).convert_alpha()
    animation_img = pygame.transform.scale(animation_img, size)
    screen.blit(animation_img, position)

def display_advice(screen, text, time_step):
    # Set the speech bubble for the text
    frame_img = pygame.image.load("Assets/Level/Character/frame.png").convert_alpha()
    frame_img = pygame.transform.scale(frame_img, (400, 145))
    screen.blit(frame_img, (50, 70))

    # Load the character's sprite
    character_paths = [
        "Assets/Level/Character/character_1.png",
        "Assets/Level/Character/character_2.png",
        "Assets/Level/Character/character_3.png"
    ]

    # Calculate which frame to display based on time _step
    frame = int((time_step + 1) % len(character_paths))

    # Display the advice on the screen
    animate_images(screen, character_paths, (65, 65), (15, 15), frame)
    path_font = "Assets/Font/pixela-extreme.ttf"
    font = pygame.font.Font(path_font, 16)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (70, 105))

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

    if level_number == 0:

        screen.fill((0, 0, 0))
        pygame.display.flip()

        story = """In 2378, in a parallel universe called Nebulaëris, the Orion System shines like a beacon in the black
        immensity. It is an oasis of life in a sea of nebulae and dead stars. You are Kornus, a talented aerospace 
        engineer. Your childhood best friend, Thorne, shares your passion for space exploration. You grew up together, 
        dreaming of traveling to the stars and discovering the secrets of the universe. But one day, your dream turns
        into a nightmare. Thorne is abducted by aliens from the planet XFE-462, a mysterious planet located in the 
        Orion System. Your world collapses around you. You can't imagine your life without Thorne. You are determined 
        to save him, no matter the cost. Using your engineering skills, you build a revolutionary rocket capable of
        traveling from planet to planet. It's a crazy bet, a suicide mission, but you're willing to do anything to 
        find your friend. Your journey will take you through the dangers of space.  But you will never give up hope.
        You know that Thorne is out there somewhere, waiting to be rescued."""

        display_text_scenario(story)
        
    if level_number == 1:
        planet_radius = 45
        orbit_radius = 130
        position = (900, 425)
        screen.blit(transparent_surface, (0, 0))

        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)


        # Load the character's text
        text = ("Drag your mouse backward to set the angle"
                "\nand power of the shot, then release it"
                "\nto launch ! You can cancel your shoot by"
                "\nright clicking when aiming !")

        display_advice(screen, text, time_step)

        return orbit_radius, position, [], []

    if level_number == 2:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)
        screen.blit(transparent_surface, (0, 0))
        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)

        # Add all the obstacles contained in the level
        obstacles = [[pygame.Rect(700, 460, 40, 40), 1], [pygame.Rect(700, 250, 40, 40), 2]]

        # Load the character's text
        text = ("Hey, watch out for the asteroids! They"
                "\ncould destroy your ship if you crash into"
                "\nthem! So you'd better do everything you can"
                "\nto avoid them !")

        display_advice(screen, text, time_step)

        return orbit_radius, position, obstacles, []

    if level_number == 3:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 250)
        screen.blit(transparent_surface, (0, 0))
        planet(transparent_surface, position, planet_radius, orbit_radius, level_number)

        # Add all the obstacles contained in the level
        obstacles = [[pygame.Rect(700, 350, 40, 40), 1], [pygame.Rect(700, 410, 40, 40), 2],
                     [pygame.Rect(760, 470, 40, 40), 3],
                     [pygame.Rect(850, 260, 40, 40), 4]]

        # Add all the objects contained in the level
        objects = [["shield", pygame.Rect(500, 500, 40, 40)],]

        # Load the character's text
        text = ("Hey, look over there! Isn't that an asteroid"
                "\nshield over there ?! Go and get it, you"
                "\nmight be able to protect your ship against"
                "\nat least one asteroid.")

        display_advice(screen, text, time_step)

        return orbit_radius, position, obstacles, objects

    if level_number == 4:
        planet_radius = 35
        orbit_radius = 85
        position = (1200, 300)
        screen.blit(transparent_surface, (0, 0))

        # Add all the obstacles contained in the level
        obstacles = []

        # Add all the objects contained in the level
        objects = []

        return orbit_radius, position, obstacles, objects
