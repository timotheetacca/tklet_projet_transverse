import pygame

scroll=15
screen_width, screen_height = 1536, 864

def level_selection(screen, background, planets, planet_rects, locked_planets, locked_planet_rects, arrows, arrow_rects,last_level):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(2 * screen_width):
        screen.blit(background, (i * (screen_width / 2), 0))
    for i in range(len(locked_planets)):
        screen.blit(locked_planets[i], (locked_planet_rects[i].x, locked_planet_rects[i].y))
    for i in range(last_level):
        screen.blit(planets[i], (planet_rects[i].x, planet_rects[i].y))
    for i in range(len(arrows)):
        screen.blit(arrows[i], (arrow_rects[i].x, arrow_rects[i].y))

    if arrow_rects[1].collidepoint(mouse_x, mouse_y):
        if planet_rects[1].x>-650:
            for planet_rect in planet_rects:
                planet_rect.x -= scroll
            for locked_planet_rect in locked_planet_rects:
                locked_planet_rect.x -= scroll
            arrow_rects[1].x = screen_width - 150
            arrow_rects[0].x = 75
    if arrow_rects[0].collidepoint(mouse_x, mouse_y):
        if planet_rects[3].x < 2900 or locked_planet_rects[2].x<2900:
            for planet_rect in planet_rects:
                planet_rect.x += scroll
            for locked_planet_rect in locked_planet_rects:
                locked_planet_rect.x += scroll
            arrow_rects[1].x = screen_width - 150
            arrow_rects[0].x = 75

    for i in range(1, len(planet_rects) + 1):
        planet_rect = planet_rects[i - 1]
        if planet_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0] == 1:
            return int(i)

    return 0