import pygame
import time

pygame.init()

screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

path_font = "Assets/Font/pixela-extreme.ttf"
font = pygame.font.Font(path_font, 30)


def display_text_scenario(story):
    j = 0
    sentence_story = story.split(". ")
    lines = []

    for i in range(len(sentence_story)):
        sentence_story[i] += "."

    while j != len(sentence_story):
        text = font.render(sentence_story[j], True, (255, 255, 255))
        text_rect = text.get_rect()

        if text_rect.width > (screen_width / 2):

            line_temp = ""
            words = sentence_story[j].split()

            for word in words:

                if font.size(line_temp + word)[0] <= screen_width:
                    line_temp += word
                else:
                    lines.append(line_temp)
                    line_temp = ""

        text_rect.height *= len(lines)
        text_rect.center = (screen_width / 2, screen_height / 2)


        screen.blit(text, text_rect)

        pygame.display.flip()

        j += 1

        time.sleep(1)
        screen.fill((0, 0, 0))
        pygame.display.flip()
