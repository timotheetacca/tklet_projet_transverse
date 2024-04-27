import pygame

def update_save_information(save_file_name):
    """
    Update the save file information.

    Parameters
    ----------
    save_file_name(str): Name of the save file

    Returns
    -------
    list(int, int) : A list containing the save informations
    """
    with open(save_file_name, 'r') as save:
        informations = save.read().strip()  # Read the content of the save file

    if not informations:
        with open(save_file_name, 'w') as save:
            save.write("0|3")  # Default: level_number=1, lives=3
        return 1, 3  # Return default values
    else:
        # If save file has content, parse and return level number and lives
        level_number, lives = informations.split("|")
        return int(level_number), int(lives)

# General functions to update level and lives

def update_lives(save_file_name, new_lives):
    """
    Update the number of lives in the save file

    Parameters
    ----------
    save_file_name(str): Name of the save file
    new_lives(int) : New number of lives

    Returns
    -------
    None
    """
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        level_number = int(informations[0])  # Get current level number

    with open(save_file_name, 'w') as save:
        save.write(f"{level_number}|{new_lives}")  # Write updated lives

def update_level(save_file_name, new_level):
    """
    Update the level number in the save file

    Parameters
    ----------
    save_file_name(str): Name of the save file
    new_level(int) : New level number

    Returns
    -------
    None
    """
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        lives = int(informations[1])  # Get current number of lives

    with open(save_file_name, 'w') as save:
        save.write(f"{new_level}|{lives}")  # Write updated level

def remove_life(save_file_name):
    """
    Remove one life from the save file

    Parameters
    ----------
    save_file_name(str) : Name of the save file

    Returns
    -------
    None
    """
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        lives = int(informations[1])  # Get current number of lives

    # Decrease lives by 1 makes sure it doesn't go below 0
    new_lives = max(0, lives - 1)
    update_lives(save_file_name, new_lives)  # Update lives in the save file

def add_level(save_file_name):
    """
    Add a level to the save file

    Parameters
    ----------
    save_file_name(str) : Name of the save file

    Returns
    -------
    list : A list containing the save informations
    """
    # Function to add a level to the save file
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        last_level = int(informations[0])  # Get current level number

    # Increase level by 1
    new_level = last_level + 1
    update_level(save_file_name, new_level)  # Update level in the save file
    return last_level, new_level

def display_life(num_lives, screen, life_image_path):
    """
    Display life images on the screen

    Parameters
    ----------
    num_lives(int) : Number of lives to display
    screen(pygame.Surface) : The pygame surface where the trajectory will be drawn
    life_image_path(str) : Path to the image file

    Returns
    -------
    None
    """
    # Load life image and resize it to 50% smaller
    life_image = pygame.image.load(life_image_path)
    life_image = pygame.transform.scale(life_image, (int(life_image.get_width() * 0.25), int(life_image.get_height() * 0.25)))

    # Get screen dimensions
    screen_width, screen_height = screen.get_size()

    # Calculate position to display images (top right)
    image_width, image_height = life_image.get_size()
    start_x = screen_width - (num_lives * (image_width + 20))
    start_y = 20

    # Display lives
    for i in range(num_lives):
        screen.blit(life_image, (start_x + i * (image_width + 20), start_y))