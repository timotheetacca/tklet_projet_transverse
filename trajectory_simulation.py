import pygame
from trajectory import draw_trajectory, draw_aim
from level import level

screen_width, screen_height = 1536, 864
fps = 120

class TrajectorySimulation:
    def __init__(self,circle_radius, screen, screen_width, screen_height ):
        self.transparent_surface = pygame.Surface((1536, 864), pygame.SRCALPHA)
        self.circle_radius = circle_radius
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def level_display(self, level_number):
        """
        Draw a level on a screen.

        Parameters
        ----------
        level_number(int) : Current level

        Returns
        -------
        orbit_radius(int) : The orbit's radius
        position(tuple) : Coordinates of the planet
        obstacles(list) : List of all the obstacles in the level
        """

        # Collect the level info and print it
        orbit_radius, position, obstacles = level(level_number, self.screen, self.transparent_surface)

        for obstacle in obstacles:
            pygame.draw.rect(self.transparent_surface, (100, 65, 23), obstacle)

        return orbit_radius, position, obstacles

    def projectile_aim(self, g, v, h, alpha, t, level_number):
        """
        Display the aim trajectory on the screen.

        Parameters
        ----------
        g(int) : Gravitational acceleration
        v(int) : Initial velocity
        h(int) : Initial height
        alpha(int) : Launch angle in degrees
        level_number(int) : Current level number

        Returns
        -------
        None
        """
        self.level_display(level_number)
        draw_aim(self.screen, g, v, h, alpha, t, self.circle_radius, self.screen_height, 22)

    def projectile_motion(self, circle_x, circle_y, g, v, h, alpha, level_number):
        """
        Display the motion of the projectile.

        Parameters
        ----------
        circle_x(int) : Initial x-coordinate
        circle_y(int) : Initial y-coordinate
        g(int) : Gravitational acceleration
        v(int) : Initial velocity
        h(int) : Initial height
        alpha(int) : Launch angle in degrees
        level_number(int) : Current level number

        Returns
        -------
        shooting_trajectory(bool) : Indicates whether the projectile is still in motion.
        level_number(int) : Updated level number if the projectile entered a new level.
        """
        # Reset timer and position for shooting
        time_step = 0
        clock = pygame.time.Clock()
        shooting_trajectory = False
        stop_level = False

        while 0 <= circle_x <= 1536 and 0 <= circle_y <= 864 and not stop_level:
            self.screen.fill((0, 0, 0))
            orbit_radius, position, obstacles = self.level_display(level_number)

            # Check for collisions with obstacles
            for obstacle in obstacles:
                if obstacle.collidepoint(circle_x, circle_y):
                    stop_level = True

            # Call the draw_trajectory function from trajectory.py
            circle_x, circle_y = draw_trajectory(self.screen, g, v, h, alpha, time_step,
                                                 self.circle_radius, self.screen_height, (255, 255, 255))

            pygame.display.update()
            time_step += clock.tick(fps) / 180  # Increment time step for the next iteration

            # Check if the projectile enters the planet's orbit
            if (circle_x - position[0]) ** 2 + (circle_y - position[1]) ** 2 <= orbit_radius ** 2:
                stop_level = True
                shooting_trajectory = False
                orbital_game_phase = True
                level_number += 1
                self.transparent_surface.fill((0, 0, 0))
                return shooting_trajectory, level_number, True

        # Reset the mouse position to avoid angle error on the next throw
        pygame.mouse.set_pos(self.screen_width // 2, self.screen_height // 2)
        self.transparent_surface.fill((0, 0, 0))

        return shooting_trajectory, level_number, False
