import pygame
import time
import os

pygame.init()

screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

path_font = "Assets/Font/pixela-extreme.ttf"
font = pygame.font.Font(path_font, 30)

skip_image = pygame.image.load('Assets/skip.png')
skip_button = pygame.transform.scale(skip_image, (150, 60))
skip_button_rect = skip_button.get_rect()
skip_button_rect.x = 1300
skip_button_rect.y = 50

cursor_image_still = pygame.image.load("Assets/Cursor/cursor_still.png")
cursor_image_hold = pygame.image.load("Assets/Cursor/cursor_hold.png")

# SPACE BAR ELEMENTS

space_bar_button = pygame.image.load("Assets/Scenario/space_bar_scenario.png")
space_bar_button = pygame.transform.scale(space_bar_button, (600, 300))
space_bar_rect = space_bar_button.get_rect()
space_bar_rect.center = (screen_width // 2, screen_height * 3 / 4)


def draw_cursor(cursor):
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(cursor, (mouse_pos[0], mouse_pos[1]))


def darken_screen(transparency_level):
    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    surface.fill((0, 0, 0, transparency_level))
    screen.blit(surface, (0, 0))


def display_text_scenario(story):
    screen_width_divided_by_two = screen_width / 2
    screen_height_divided_by_two = screen_height / 2
    j = 0
    sentence_story = story.split(". ")
    number_of_sentences = len(sentence_story)
    rect = pygame.Rect(0, 0, 0, 0)
    rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
    white = (255, 255, 255)
    transparency = 0
    go_to_next_message = True
    displaying_text = False
    screen_fill_black_time = True
    cursor = pygame.transform.scale(cursor_image_still, (32, 32))

    for i in range(number_of_sentences - 1):
        sentence_story[i] += "."

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor = pygame.transform.scale(cursor_image_hold, (32, 32))
                if skip_button_rect.collidepoint(event.pos):
                    return

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor = pygame.transform.scale(cursor_image_still, (32, 32))

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not displaying_text:
                j += 1  # Move to the next sentence
                go_to_next_message = True

        if j < number_of_sentences:

            if screen_fill_black_time:
                screen.fill((0, 0, 0))
            else:
                screen.blit(background, (0, 0))

            screen.blit(skip_button, skip_button_rect)
            if j < 2:
                screen.blit(space_bar_button, (space_bar_rect))
            text = font.render(sentence_story[j], True, white)
            text_rect = text.get_rect()

            if go_to_next_message:
                displaying_text = True
                screen.fill((0, 0, 0))
                if text_rect.width > screen_width_divided_by_two:
                    lines = []
                    line_temp = ""
                    words = sentence_story[j].split()

                    for word in words:

                        if font.size(line_temp + word + " ")[0] <= screen_width_divided_by_two:
                            line_temp += word + " "

                        else:
                            lines.append(line_temp)
                            line_temp = word + " "

                    if line_temp:
                        lines.append(line_temp)

                    rect.height = 0
                    rect.width = screen_width_divided_by_two

                    for line in lines:
                        line_surface = font.render(line, True, white)
                        rect.height += line_surface.get_rect().height

                    rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
                    rect.topleft = (screen_width_divided_by_two / 2, (screen_height - rect.height) / 2)

                    height_line = 0
                    for line in lines:
                        for i in range(len(line) + 1):
                            displayed_text = line[:i]
                            displayed_text_surface = font.render(displayed_text, True, white)
                            displayed_text_rect = displayed_text_surface.get_rect(
                                topleft=(rect.topleft[0], rect.topleft[1] + height_line))
                            screen.blit(displayed_text_surface, displayed_text_rect)
                            pygame.display.flip()
                            time.sleep(0.020)
                        height_line += displayed_text_rect.height

                else:
                    text_rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
                    for i in range(len(sentence_story[j]) + 1):
                        displayed_text = sentence_story[j][:i]
                        displayed_text_surface = font.render(displayed_text, True, white)
                        displayed_text_rect = text_rect
                        screen.blit(displayed_text_surface, displayed_text_rect)
                        pygame.display.flip()
                        time.sleep(0.020)

                screen_capture = pygame.Surface((screen_width, screen_height))
                screen_capture.blit(screen, (0, 0))
                os.remove('Assets/Scenario/screen_capture_with_text_scenario.png')
                pygame.image.save(screen_capture, 'Assets/Scenario/screen_capture_with_text_scenario.png')
                background = pygame.image.load("./Assets/Scenario/screen_capture_with_text_scenario.png")
                screen.blit(background, (0, 0))
                screen_fill_black_time = False

                go_to_next_message = False
            else:
                displaying_text = False

            draw_cursor(cursor)

        else:
            time.sleep(0.5)
            fading = True
            while fading:
                darken_screen(transparency)
                transparency += 1
                pygame.display.flip()
                if transparency >= 255:
                    fading = False
            return

        pygame.display.flip()
