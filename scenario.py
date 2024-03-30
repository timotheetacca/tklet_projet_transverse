import pygame
import time

pygame.init()

screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

path_font = "Assets/Font/pixela-extreme.ttf"
font = pygame.font.Font(path_font, 30)


def display_text_scenario(story, time_message):
    screen_width_divided_by_two = screen_width / 2
    j = 0
    sentence_story = story.split(". ")
    rect = pygame.Rect(0, 0, 0, 0)
    rect.center = (screen_width_divided_by_two, screen_height / 2)
    white = (255, 255, 255)

    for i in range(len(sentence_story) - 1):
        sentence_story[i] += "."

    while j != len(sentence_story):
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
            rect.center = (screen_width_divided_by_two, screen_height / 2)

            for line in lines:
                line_surface = font.render(line, True, white)
                rect.height += line_surface.get_rect().height

            height_line = 0
            for line in lines:
                line_surface = font.render(line, True, white)
                line_rect = line_surface.get_rect()
                line_rect.topleft = (rect.topleft[0], rect.topleft[1] + height_line)
                height_line += line_rect.height
                screen.blit(line_surface, line_rect)
        else:
            text_rect.center = (screen_width_divided_by_two, screen_height / 2)
            screen.blit(text, text_rect)

        j += 1
        pygame.display.flip()

        time.sleep(time_message)

        screen.fill((0, 0, 0))
        pygame.display.flip()
