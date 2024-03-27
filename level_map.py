import pygame

scroll=3
screen_width, screen_height = 1536, 864

def level_selection(screen, background, planets, planet_rects, arrows, arrow_rects):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(2 * screen_width):
        screen.blit(background, (i * (screen_width / 2), 0))
    for planet, rect in zip(planets, planet_rects):
        screen.blit(planet, (rect.x, rect.y))
    for arrow, arrow_rect in zip(arrows, arrow_rects):
        screen.blit(arrow, (arrow_rect.x, arrow_rect.y))

    if arrow_rects[1].collidepoint(mouse_x, mouse_y):
        for planet_rect in planet_rects:
            planet_rect.x -= scroll
        arrow_rects[1].x = screen_width - 150
        arrow_rects[0].x = 75
    if arrow_rects[0].collidepoint(mouse_x, mouse_y):
        for planet_rect in planet_rects:
            planet_rect.x += scroll
        arrow_rects[1].x = screen_width - 150
        arrow_rects[0].x = 75

    for i, planet_rect in enumerate(planet_rects, start=1):
        if planet_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0] == 1:
            return True, i

    return False, 0