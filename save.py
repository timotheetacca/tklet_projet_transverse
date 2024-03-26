def update_save_information(save_file_name):
    # Function to read and update save file information
    with open(save_file_name, 'r') as save:
        informations = save.read().strip()  # Read the content of the save file

    # If save file is empty, initialize with default values and return
    if not informations:
        with open(save_file_name, 'w') as save:
            save.write("1|3")  # Default: level_number=1, lives=3
        return 1, 3  # Return default values
    else:
        # If save file has content, parse and return level number and lives
        level_number, lives = informations.split("|")
        return int(level_number), int(lives)

# General functions to update level and lives

def update_lives(save_file_name, new_lives):
    # Function to update lives in the save file
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        level_number = int(informations[0])  # Get current level number

    # Write updated information (level_number unchanged)
    with open(save_file_name, 'w') as save:
        save.write(f"{level_number}|{new_lives}")  # Write updated lives

def update_level(save_file_name, new_level):
    # Function to update level in the save file
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        lives = int(informations[1])  # Get current number of lives

    # Write updated information (lives unchanged)
    with open(save_file_name, 'w') as save:
        save.write(f"{new_level}|{lives}")  # Write updated level

# Remove 1 life using update level functions
def remove_life(save_file_name):
    # Function to remove a life from the save file
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        lives = int(informations[1])  # Get current number of lives

    # Decrease lives by 1, ensuring it doesn't go below 0
    new_lives = max(0, lives - 1)
    update_lives(save_file_name, new_lives)  # Update lives in the save file

# Add 1 level using update functions
def add_level(save_file_name):
    # Function to add a level to the save file
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        level_number = int(informations[0])  # Get current level number

    # Increase level by 1
    new_level = level_number + 1
    update_level(save_file_name, new_level)  # Update level in the save file
