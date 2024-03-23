def update_save_information(save_file_name):
    with open(save_file_name, 'r') as save:
        informations = save.read().strip()

    if not informations:
        with open(save_file_name, 'w') as save:
            save.write("1|3")
        return 1,3 #level_number, lives
    else:
        level_number, lives = informations.split("|")
        return int(level_number), int(lives)

# Update level and lives
def update_lives(save_file_name,new_lives):
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        level_number = int(informations[0])
    with open(save_file_name, 'w') as save:
        save.write(f"{level_number}|{new_lives}")

def update_level(save_file_name,new_level):
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        lives = int(informations[1])
    with open(save_file_name, 'w') as save:
        save.write(f"{new_level}|{lives}")

# Remove 1 life using update level functions
def remove_life(save_file_name):
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        lives = int(informations[1])
    new_lives = max(0, lives - 1)  # Ensure lives doesn't go below 0
    update_lives(save_file_name, new_lives)

# Add 1 level using update functions
def add_level(save_file_name):
    with open(save_file_name, 'r') as save:
        informations = save.read().strip().split("|")
        level_number = int(informations[0])
    new_level = level_number + 1
    update_level(save_file_name, new_level)
