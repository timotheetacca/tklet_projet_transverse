import re
import pygame
import time
import os

# Initialize pygame
pygame.init()

# Set up the screen dimensions
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))

# Path to the font file
path_font = "Assets/Font/pixela-extreme.ttf"
font = pygame.font.Font(path_font, 30)

# Load skip button image and scale it
skip_image = pygame.image.load('Assets/skip.png')
skip_button = pygame.transform.scale(skip_image, (150, 75))
skip_button_rect = skip_button.get_rect()
coord_skip_button = (screen_width - 175, 95)
skip_button_rect = skip_button.get_rect(bottomleft=coord_skip_button)

# Load cursor images
cursor_image_still = pygame.image.load("Assets/Cursor/cursor_still.png")
cursor_image_hold = pygame.image.load("Assets/Cursor/cursor_hold.png")

# Load space bar button image and scale it
space_bar_button = pygame.image.load("Assets/Scenario/space_bar_scenario.png")
space_bar_button = pygame.transform.scale(space_bar_button, (350, 75))
space_bar_rect = space_bar_button.get_rect()
space_bar_rect.center = (screen_width // 2, screen_height * 3 / 4)


def draw_cursor(cursor):
    """
    Draw the cursor on the screen

    Parameters
    ----------
    cursor(pygame.image.load) : the cursor to be displayed

    Returns
    -------
    None
    """
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(cursor, (mouse_pos[0], mouse_pos[1]))


# Function to darken the screen with a given transparency level
def darken_screen(transparency_level):
    """
    Darken the screen with a given transparency level

    Parameters
    ----------
    transparency_level(int) : The transparency level for darkening the screen.

    Returns
    -------
    None
    """

    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    surface.fill((0, 0, 0, transparency_level))
    screen.blit(surface, (0, 0))


def clean_story(story):
    """
    Remove the \n from a text

    Parameters
    ----------
    story(string) : The story of the game

    Returns
    -------
    story
    """
    for i in range(story.count("\n")):
        story.replace("\n", "")

    return story


# Function to display the text scenario
def display_text_scenario(story, background, skip_allowed=True, fade_out=True):
    """
    Display the text scenario

    Parameters
    ----------
    story(str) : The text scenario to be displayed.

    Returns
    -------
    None
    """

    story = clean_story(story)
    screen_width_divided_by_two = screen_width / 2
    screen_height_divided_by_two = screen_height / 2
    j = 0
    sentence_story = re.split(r'[.!?]', story)  # Allow to split with . or !
    rect = pygame.Rect(0, 0, 0, 0)
    rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
    white = (255, 255, 255)
    transparency = 0
    go_to_next_message = True
    displaying_text = False
    screen_fill_black_time = True
    cursor = pygame.transform.scale(cursor_image_still, (32, 32))
    background_temp = background

    # Load background music
    pygame.mixer.music.load("Assets/Scenario/sound_message_appearing.mp3")
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    pygame.mixer.music.set_volume(0.25)

    for i in range(sentence_story.count("")):
        sentence_story.remove("")

    number_of_sentences = len(sentence_story)

    if '!' in story:
        for i in range(number_of_sentences):
            sentence_story[i] += "!"
    elif '.' in story:
        for i in range(number_of_sentences):
            sentence_story[i] += "."
    elif '?' in story:
        for i in range(number_of_sentences):
            sentence_story[i] += "?"

    # Loop until all sentences are displayed or the user quits
    while True:

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor = pygame.transform.scale(cursor_image_hold, (32, 32))
                if skip_button_rect.collidepoint(event.pos) and skip_allowed:
                    return
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor = pygame.transform.scale(cursor_image_still, (32, 32))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not displaying_text:
                j += 1  # Move to the next sentence
                go_to_next_message = True

        if j <= number_of_sentences - 1:

            # Display either a black screen or background image
            if screen_fill_black_time:
                screen.fill((0, 0, 0))
            else:
                screen.blit(background_temp, (0, 0))

            if skip_allowed:
                screen.blit(skip_button, skip_button_rect)

            # Display space bar button for the first two sentences
            if j < 2:
                screen.blit(space_bar_button, space_bar_rect)

            # Render and display text
            text = font.render(sentence_story[j], True, white)
            text_rect = text.get_rect()

            if go_to_next_message:
                displaying_text = True
                screen.blit(background, (0, 0))

                pygame.mixer.music.unpause()

                # Split the text into lines if it's too wide
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

                    # Calculate the position of each line
                    rect.height = 0
                    rect.width = screen_width_divided_by_two

                    for line in lines:
                        line_surface = font.render(line, True, white)
                        rect.height += line_surface.get_rect().height

                    rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
                    rect.topleft = (
                        (screen_width_divided_by_two / 2) + screen_width / 90, (screen_height - rect.height) / 2)

                    height_line = 0
                    # Display the text letter by letter
                    for line in lines:
                        for i in range(len(line) + 1):
                            displayed_text = line[:i]
                            displayed_text_surface = font.render(displayed_text, True, white)
                            displayed_text_rect = displayed_text_surface.get_rect(
                                topleft=(rect.topleft[0], rect.topleft[1] + height_line))
                            screen.blit(displayed_text_surface, displayed_text_rect)
                            pygame.display.flip()
                            time.sleep(0.013)
                        height_line += displayed_text_rect.height

                # If the text fits the screen width, display it letter by letter
                else:
                    text_rect.center = (screen_width_divided_by_two, screen_height_divided_by_two)
                    for i in range(len(sentence_story[j]) + 1):
                        displayed_text = sentence_story[j][:i]
                        displayed_text_surface = font.render(displayed_text, True, white)
                        displayed_text_rect = text_rect
                        screen.blit(displayed_text_surface, displayed_text_rect)
                        pygame.display.flip()
                        time.sleep(0.013)

                pygame.mixer.music.pause()

                # Capture the screen with the displayed text and save it
                screen_capture = pygame.Surface((screen_width, screen_height))
                screen_capture.blit(screen, (0, 0))
                os.remove('Assets/Scenario/screen_capture_with_text_scenario.png')
                pygame.image.save(screen_capture, 'Assets/Scenario/screen_capture_with_text_scenario.png')
                background_temp = pygame.image.load("./Assets/Scenario/screen_capture_with_text_scenario.png")
                screen.blit(background_temp, (0, 0))
                screen_fill_black_time = False
                go_to_next_message = False
            else:
                displaying_text = False

            draw_cursor(cursor)

        elif fade_out and j == number_of_sentences:
            # If all sentences are displayed, fade out the screen
            time.sleep(0.5)
            fading = True
            while fading:
                darken_screen(transparency)
                transparency += 1
                pygame.display.flip()
                if transparency >= 255:
                    fading = False
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            return

        elif not fade_out and j == number_of_sentences:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            return

        pygame.display.flip()
