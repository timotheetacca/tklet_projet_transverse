import pygame

scroll = 30
screen_width, screen_height = 1536, 864
left_click = False

def level_selection(screen, background, planets, planet_rects, locked_planets, locked_planet_rects, arrows, arrow_rects,last_level):
    """
    Display the level selection screen and handle user input for selecting levels

    Parameters
    ----------
    screen(pygame.Surface) : The pygame surface where the level selection screen will be drawn
    background(pygame.Surface) : The background image for the level selection screen
    planets(list) : List of planet images representing unlocked levels
    planet_rects(list) : List of pygame.Rect objects representing the positions of unlocked planets
    locked_planets(list) : List of planet images representing locked levels
    locked_planet_rects(list) : List of pygame.Rect objects representing the positions of locked planets
    arrows(list[pygame.Surface]) : List of arrow images for scrolling the level selection screen
    arrow_rects(list) : List of pygame.Rect objects representing the positions of arrow buttons
    last_level(int) : The index of the last unlocked level.

    Returns
    -------
    int
        The index of the selected level, or 0 if no level is selected.
    """
    global left_click
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw background
    for i in range(2 * screen_width):
        screen.blit(background, (i * (screen_width / 2), 0))

    # Draw locked planets
    for i in range(last_level - 1, len(locked_planets)):
        screen.blit(locked_planets[i], (locked_planet_rects[i].x, locked_planet_rects[i].y))

    # Draw unlocked planets
    for i in range(last_level):
        screen.blit(planets[i], (planet_rects[i].x, planet_rects[i].y))

    # Draw arrows for scrolling
    for i in range(len(arrows)):
        screen.blit(arrows[i], (arrow_rects[i].x, arrow_rects[i].y))

    # Handle left scrolling arrow click
    if arrow_rects[1].collidepoint(mouse_x, mouse_y):
        if planet_rects[1].x > -2125:
            for planet_rect in planet_rects:
                planet_rect.x -= scroll
            for locked_planet_rect in locked_planet_rects:
                locked_planet_rect.x -= scroll
            arrow_rects[1].x = screen_width - 150
            arrow_rects[0].x = 75

    # Handle right scrolling arrow click
    if arrow_rects[0].collidepoint(mouse_x, mouse_y):
        if planet_rects[len(planets)-1].x < 3450 or locked_planet_rects[len(locked_planets)-2].x < 3450:
            for planet_rect in planet_rects:
                planet_rect.x += scroll
            for locked_planet_rect in locked_planet_rects:
                locked_planet_rect.x += scroll
            arrow_rects[1].x = screen_width - 150
            arrow_rects[0].x = 75

    # Allow to enter the level only if the left click button is released
    for i in range(1, len(planet_rects) + 1):
        planet_rect = planet_rects[i - 1]
        if planet_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0] == 1:
                left_click = True
            elif pygame.mouse.get_pressed()[0] == 0 and left_click:
                left_click = False
                return int(i)

    return 0
