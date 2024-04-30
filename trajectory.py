import pygame
import math

def calculate_trajectory(g, v, h, alpha, t, screen_height):
    """
    Calculate the x and y coordinates of a projectile's trajectory at a given time

    Parameters
    ----------
    g(float) : Gravitational acceleration
    v(float) : Initial velocity
    h(float) : Initial height
    alpha(float) : Launch angle in degrees
    t(float) : Time
    screen_height(int) : Height of the screen

    Returns
    -------
    A tuple containing the coordinates x and y
    """
    # Removes the screens height for trajectory to appear on the bottom
    y = screen_height - int((-1 / 2) * g * t ** 2 + v * math.sin(math.radians(alpha)) * t + h)
    x = int(v * math.cos(math.radians(alpha)) * t)
    return x, y


def draw_trajectory(screen, g, v, h, alpha, t, screen_height, portal, teleport,portal_input=[], portal_output=[]):
    """
    Draw a trajectory on a given pygame surface.

    Parameters
    ----------
    screen(pygame.Surface) : The pygame surface where the trajectory will be drawn
    g(float) : Gravitational acceleration
    v(float) : Initial velocity
    h(float) : Initial height
    alpha(float) : Launch angle in degrees
    t(float) : Time
    screen_height(int) : Height of the screen
    portal(bool) : True if there is a portal, False if not
    teleport(bool) : True if the rocket has been teleported
    portal_input(list) : List of infos about the input portal
    portal_output(list): List of infos about the ouput portal

    Returns
    -------
    rocket_x, rocket_y (int) : Coordinates of the rocket
    """
    rocket_x, rocket_y = calculate_trajectory(g, v, h, alpha, t, screen_height)

    if portal:
        square_rect = pygame.Rect(portal_input[0], portal_input[1], portal_input[2], portal_input[2])
        if square_rect.collidepoint(rocket_x, rocket_y):
            teleport = True

        if teleport:
            rocket_x += (portal_output[0]-portal_input[0])
            rocket_y -= (portal_input[1]-portal_output[1])

    # Load the rocket image
    rocket_image = pygame.image.load('Assets/rocket.png')
    rocket_image = pygame.transform.scale(rocket_image, (44,30))

    # Calculate the angle of the trajectory in degree at the current point
    trajectory_angle = math.degrees(math.atan2(-g * t + v * math.sin(math.radians(alpha)), v * math.cos(math.radians(alpha))))

    # Rotate the rocket image based on the trajectory angle
    rotated_rocket = pygame.transform.rotate(rocket_image, trajectory_angle)

    # Get the rectangle for the rotated image
    rocket_rect = rotated_rocket.get_rect(center=(rocket_x, rocket_y))

    screen.blit(rotated_rocket, rocket_rect)

    return rocket_x, rocket_y, teleport


def draw_aim(screen, g, v, h, alpha, circle_radius, screen_height, nb_points):
    """
    Draw a trajectory for aiming on a given pygame surface.

    Parameters
    ----------
    screen(pygame.Surface) : The pygame surface where the trajectory will be drawn
    g(float) : Gravitational acceleration
    v(float) : Initial velocity
    h(float) : Initial height
    alpha(float) : Launch angle in degrees
    circle_radius(int) : Radius of the circle to be drawn
    screen_height(int) : Height of the screen
    nb_points(int) : The number of points display

    Returns
    -------
    None
    """
    # Draw the rocket with the corresponding angle of launch
    rocket_image = pygame.image.load('Assets/rocket.png')
    rocket_image = pygame.transform.scale(rocket_image, (44,30))
    trajectory_angle = math.degrees(math.atan2(-g + v * math.sin(math.radians(alpha)), v * math.cos(math.radians(alpha))))
    rotated_rocket = pygame.transform.rotate(rocket_image, trajectory_angle)
    screen.blit(rotated_rocket, (0,820))

    for t in range(1,nb_points):
        rocket_x, rocket_y = calculate_trajectory(g, v, h, alpha, t / 2, screen_height)
        # Reduce the radius of the circle to make the aiming less and less visible
        pygame.draw.circle(screen, (250, 250, 250), (rocket_x + 20, rocket_y - 20), circle_radius - 0.1 * t)
