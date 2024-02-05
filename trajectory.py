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
    circle_y = screen_height - int((-1/2) * g * t**2 + v * math.sin(math.radians(alpha)) * t + h)
    circle_x = int (v * math.cos(math.radians(alpha)) * t)
    return circle_x, circle_y

def draw_trajectory(screen, g, v, h, alpha, t, circle_radius, screen_height):
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

    Returns
    -------
    None
    """
    circle_x, circle_y = calculate_trajectory(g, v, h, alpha, t, screen_height)
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), circle_radius)
