import pygame
import time

pygame.init()

screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

path_font = "Assets/Font/pixela-extreme.ttf"
font = pygame.font.Font(path_font, 30)


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

    for i in range(number_of_sentences - 1):
        sentence_story[i] += "."

    while j != number_of_sentences:
        text = font.render(sentence_story[j], True, white)
        text_rect = text.get_rect()

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
                    time.sleep(0.025)
                height_line += displayed_text_rect.height
        else:
            text_rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
            for i in range(len(sentence_story[j]) + 1):
                displayed_text = sentence_story[j][:i]
                displayed_text_surface = font.render(displayed_text, True, white)
                displayed_text_rect = text_rect
                screen.blit(displayed_text_surface, displayed_text_rect)
                pygame.display.flip()
                time.sleep(0.025)

        fully_displayed = True

        while fully_displayed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and fully_displayed:
                        j += 1
                        fully_displayed = False
                        break

        if j == number_of_sentences:
            time.sleep(0.5)
            fading = True
            while fading:
                darken_screen(transparency)
                transparency += 1
                pygame.display.flip()
                if transparency >= 255:
                    fading = False

        screen.fill((0, 0, 0))
        pygame.display.flip()
