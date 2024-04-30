import pygame
import math

def calculate_trajectory(g, v, h, alpha, t, screen_height):
    """
    Calculate the x and y coordinates of a projectile's trajectory at a given time.

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
    A tuple containing the x and y coordinates of the projectile.
    """
    # Removes the screens height for trajectory to appear on the bottom
    circle_y = screen_height - int((-1 / 2) * g * t ** 2 + v * math.sin(math.radians(alpha)) * t + h)
    circle_x = int(v * math.cos(math.radians(alpha)) * t)
    return circle_x, circle_y


def draw_trajectory(screen, g, v, h, alpha, t, circle_radius, screen_height, color, portal, teleport,portal_input=[], portal_output=[]):
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
    circle_radius(int) : Radius of the circle to be drawn
    screen_height(int) : Height of the screen
    color(int) : Color of the ball

    Returns
    -------
    circle_x, circle_y (int) : Coordinates of the circle
    """
    circle_x, circle_y = calculate_trajectory(g, v, h, alpha, t, screen_height)

    if portal:
        square_rect = pygame.Rect(portal_input[0], portal_input[1], portal_input[2], portal_input[2])
        if square_rect.collidepoint(circle_x, circle_y):
            teleport = True

        if teleport:
            circle_x += (portal_output[0]-portal_input[0])
            circle_y -= (portal_input[1]-portal_output[1])

    pygame.draw.circle(screen, color, (circle_x, circle_y), circle_radius)
    return circle_x, circle_y, teleport


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
    t(float) : Time
    circle_radius(int) : Radius of the circle to be drawn
    screen_height(int) : Height of the screen
    nb_points(int) : The number of points display

    Returns
    -------
    None
    """
    for t in range(nb_points):
        circle_x, circle_y = calculate_trajectory(g, v, h, alpha, t / 2, screen_height)
        # Reduce the radius of the circle to make the aiming less and less visible
        pygame.draw.circle(screen, (250, 250, 250), (circle_x + 20, circle_y - 20), circle_radius - 0.1 * t)
