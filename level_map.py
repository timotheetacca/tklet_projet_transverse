import pygame

scroll = 30
screen_width, screen_height = 1536, 864
left_click = False

def level_selection(screen, background, planets, planet_rects, locked_planets, locked_planet_rects, arrows, arrow_rects,last_level):
    global left_click
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i in range(2 * screen_width):
        screen.blit(background, (i * (screen_width / 2), 0))
    for i in range(last_level - 1, len(locked_planets)):
        screen.blit(locked_planets[i], (locked_planet_rects[i].x, locked_planet_rects[i].y))
    for i in range(last_level):
        screen.blit(planets[i], (planet_rects[i].x, planet_rects[i].y))
    for i in range(len(arrows)):
        screen.blit(arrows[i], (arrow_rects[i].x, arrow_rects[i].y))

    if arrow_rects[1].collidepoint(mouse_x, mouse_y):
        if planet_rects[1].x > -1425:
            for planet_rect in planet_rects:
                planet_rect.x -= scroll
            for locked_planet_rect in locked_planet_rects:
                locked_planet_rect.x -= scroll
            arrow_rects[1].x = screen_width - 150
            arrow_rects[0].x = 75
    if arrow_rects[0].collidepoint(mouse_x, mouse_y):
        print(len(planets))
        print(len(locked_planets))
        if planet_rects[len(planets)-1].x < 2750 or locked_planet_rects[len(locked_planets)-2].x < 2750:
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
