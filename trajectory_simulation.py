import pygame
from trajectory import draw_trajectory, draw_aim
from level import level
from save import add_level

screen_width, screen_height = 1536, 864
fps = 120

class TrajectorySimulation:
    def __init__(self, circle_radius, screen, screen_width, screen_height, background_image):
        self.transparent_surface = pygame.Surface((1536, 864), pygame.SRCALPHA)
        self.circle_radius = circle_radius
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    def level_display(self, level_number, full_level,time_step ,modified_obstacles=[]):
        """
        Draw a level on a screen.

        Parameters
        ----------
        level_number(int) : Current level
        full_level(bool) : Indicates whether the level should be fully displayed
        time_step(int) : Current frame for character animation
        modified_obstacles(list, optional) : List of modified obstacles

        Returns
        -------
        orbit_radius(int) : The orbit's radius
        position(tuple) : Coordinates of the planet
        obstacles(list) : List of all the obstacles in the level
        """
        # Paths to the asteroid images
        asteroid_paths = [
            "Assets/Level/Asteroids/asteroid_1.png",
            "Assets/Level/Asteroids/asteroid_2.png",
            "Assets/Level/Asteroids/asteroid_3.png",
            "Assets/Level/Asteroids/asteroid_4.png"
        ]

        # Load asteroid images
        asteroid_images = []
        for path in asteroid_paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (48, 48))
            asteroid_images.append(img)

        # Index to keep track of current asteroid image
        asteroid_index = 0

        # Collect the level info and print it
        orbit_radius, position, obstacles, objects = level(level_number, self.screen, self.transparent_surface, time_step)

        if len(obstacles) > len(modified_obstacles) and not full_level:
            for obstacle in modified_obstacles:
                # Draw scaled asteroid image instead of rectangle
                self.transparent_surface.blit(asteroid_images[asteroid_index], obstacle)
                # Move to the next asteroid image
                asteroid_index = (asteroid_index + 1) % len(asteroid_images)
        else:
            for obstacle in obstacles:
                # Draw scaled asteroid image instead of rectangle
                self.transparent_surface.blit(asteroid_images[asteroid_index], obstacle)
                # Move to the next asteroid image
                asteroid_index = (asteroid_index + 1) % len(asteroid_images)

        for object in objects:
            # Draw a shield icon for objects
            if object[0] == "shield":
                # Load and blit shield icon
                shield_icon_img = pygame.image.load("Assets/Level/Items/shield_icon.png").convert_alpha()
                shield_icon_img = pygame.transform.scale(shield_icon_img, (40, 40))
                self.transparent_surface.blit(shield_icon_img, object[1])
            else:
                # Draw rectangles for other objects
                pygame.draw.rect(self.transparent_surface, (169, 169, 169), object)

        return orbit_radius, position, obstacles, objects

    def projectile_aim(self, g, v, h, alpha, time_step, level_number):
        """
        Display the aim trajectory on the screen.

        Parameters
        ----------
        g(int) : Gravitational acceleration
        v(int) : Initial velocity
        h(int) : Initial height
        alpha(int) : Launch angle in degrees
        time_step(int): Current frame for character animation
        level_number(int) : Current level number

        Returns
        -------
        None
        """
        self.screen.blit(self.background_image, (0, 0))
        self.level_display(level_number, True, time_step)
        draw_aim(self.screen, g, v, h, alpha, self.circle_radius, self.screen_height, 22)

    def projectile_motion(self, circle_x, circle_y, g, v, h, alpha, level_number, level_attempts, clock):
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
        level_attempts(int) : Number of attempts on the current level

        Returns
        -------
        shooting_trajectory(bool) : Indicates whether the projectile is still in motion
        bool : Indicates whether the projectile has successfully hit the target
        level_attemps(int) : Number of attempts in the level
        """

        # Reset timer and position for shooting
        time_step = 0
        shooting_trajectory = False
        stop_level = False
        object_status = False

        orbit_radius, position, obstacles, objects = self.level_display(level_number, True, time_step)

        # 'For' loop to avoid code locking with while and optimization in case of bugs, will stop after 1000 steps
        for steps in range(1000):
            # Stops if the level is finished
            if not (0 <= circle_x <= screen_width and 0 <= circle_y <= screen_height) or stop_level:
                level_attempts += 1
                return shooting_trajectory, False, level_attempts

            self.screen.blit(self.background_image, (0, 0))
            self.level_display(level_number, False, time_step,obstacles)

            # Check for collisions with obstacles
            for obstacle in obstacles:
                if obstacle.collidepoint(circle_x, circle_y):
                    if not object_status:
                        stop_level = True
                        level_attempts += 1

                    else:
                        # Removes the obstacle if it touched with an object
                        obstacles.remove(obstacle)
                        self.transparent_surface.blit(self.background_image, (0, 0))
                        object_status = False

            # Check for collisions with objects
            for object in objects:
                if object[1].collidepoint(circle_x, circle_y):
                    object_status = True

            # Draw a circle around the ball to indicate it has an object
            if object_status:
                shield_image = (pygame.image.load('Assets/Level/Items/shield.png'))
                shield_image = pygame.transform.scale(shield_image, (50, 50))
                shield_rect = shield_image.get_rect(center=(circle_x, circle_y))
                self.screen.blit(shield_image, shield_rect)

            # Call the draw_trajectory function from trajectory.py
            circle_x, circle_y = draw_trajectory(self.screen, g, v, h, alpha, time_step,
                                                 self.circle_radius, self.screen_height, (255, 255, 255))

            pygame.display.update()
            time_step += clock.tick(fps) / 180  # Increment time step for the next iteration

            # Check if the projectile enters the planet's orbit
            if (circle_x - position[0]) ** 2 + (circle_y - position[1]) ** 2 <= orbit_radius ** 2:
                stop_level = True
                shooting_trajectory = False
                self.transparent_surface.blit(self.background_image, (0, 0))
                add_level("game_save.txt")
                return shooting_trajectory, True, level_attempts

        return shooting_trajectory, False, level_attempts
