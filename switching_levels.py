import pygame
from trajectory_simulation import TrajectorySimulation

pygame.init()

screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
trajectory_simulation = TrajectorySimulation(5, screen, screen_width, screen_height)

background_image = pygame.image.load("Assets/Cinematic/background.jpg").convert()
background = pygame.transform.scale(background_image, (screen_width // 2, screen_height))

planet1_image = pygame.image.load("Assets/Switch_Level/planet1.png").convert_alpha()
planet1 = pygame.transform.scale(planet1_image, (250,250))
planet1_rect = planet1.get_rect()
original_planet1_x = 250
planet1_rect.x = 250
planet1_rect.y = screen_height/2-150

planet2_image = pygame.image.load("Assets/Switch_Level/planet2.png").convert_alpha()
planet2 = pygame.transform.scale(planet2_image, (250,250))
planet2_rect = planet2.get_rect()
planet2_rect.x = planet1_rect.x+500
planet2_rect.y = planet1_rect.y

planet3_image = pygame.image.load("Assets/Switch_Level/planet3.png").convert_alpha()
planet3 = pygame.transform.scale(planet3_image, (250,250))
planet3_rect = planet3.get_rect()
original_planet3_x = 1250
planet3_rect.x = planet2_rect.x+500
planet3_rect.y = planet2_rect.y

left_arrow_image = pygame.image.load("Assets/Switch_Level/left_arrow.png").convert_alpha()
left_arrow = pygame.transform.scale(left_arrow_image, (100,80))
left_arrow_rect = left_arrow.get_rect()
left_arrow_rect.x = 75
left_arrow_rect.y = screen_height / 2-60

right_arrow_image = pygame.image.load("Assets/Switch_Level/right_arrow.png").convert_alpha()
right_arrow = pygame.transform.scale(right_arrow_image, (100,80))
right_arrow_rect = right_arrow.get_rect()
right_arrow_rect.x = screen_width-150
right_arrow_rect.y = screen_height / 2-60

level1=False
level2=False
level3=False

scroll = 3

run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i in range(2 * screen_width):
        screen.blit(background, (i * (screen_width / 2), 0))

    screen.blit(planet1, (planet1_rect.x,planet1_rect.y))
    screen.blit(planet2, (planet2_rect.x,planet2_rect.y))
    screen.blit(planet3, (planet3_rect.x, planet3_rect.y))
    screen.blit(right_arrow, (right_arrow_rect.x,right_arrow_rect.y))
    screen.blit(left_arrow, (left_arrow_rect.x, left_arrow_rect.y))

    if right_arrow_rect.collidepoint(mouse_x, mouse_y):
        planet1_rect.x-=scroll
        planet2_rect.x-=scroll
        planet3_rect.x-=scroll
        right_arrow_rect.x = screen_width-150
        left_arrow_rect.x = 75

    if left_arrow_rect.collidepoint(mouse_x, mouse_y):
        planet1_rect.x += scroll
        planet2_rect.x += scroll
        planet3_rect.x += scroll
        right_arrow_rect.x = screen_width - 150
        left_arrow_rect.x = 75

    if planet1_rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0] == 1:
            level1=True
    if planet2_rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0] == 1:
            level2=True
    if planet3_rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0] == 1:
            level3=True
    if level1:
        screen.fill((0, 0, 0))
        trajectory_simulation.level_display(1)
    if level2:
        screen.fill((0, 0, 0))
        trajectory_simulation.level_display(2)
    if level3:
        screen.fill((0, 0, 0))
        trajectory_simulation.level_display(3)

    pygame.display.update()

pygame.quit()



