import pygame

class Slider:
    def __init__(self, slider_position, slider_width, min_value, max_value, initial_value):
        self.slider_position = slider_position
        self.slider_width = slider_width
        self.min_value = min_value
        self.max_value = max_value
        self.slider_value = initial_value
        self.initial_value = initial_value
        self.handle_radius = 10
        self.dragging = False
        self.font = pygame.font.Font("Assets/Font/pixela-extreme.ttf", 16)
        self.text_position = (self.slider_position[0], self.slider_position[1] + 20)

    def draw(self, screen):
        """
        Draw the slider on the screen

        Parameters
        ----------
        screen(pygame.Surface) : The pygame surface where the trajectory will be drawn

        Returns
        -------
        None
        """
        # Calculate the slider's position and size
        slider_rect = pygame.Rect(self.slider_position[0], self.slider_position[1], self.slider_width, 10)
        handle_center = (self.slider_position[0] + int((self.slider_value - self.min_value) / (self.max_value - self.min_value) * self.slider_width), self.slider_position[1] + 5)

        # Draw the slider bar
        pygame.draw.rect(screen, (200, 200, 200), slider_rect)

        # Draw the handle
        pygame.draw.circle(screen, (100, 100, 100), handle_center, self.handle_radius)

        # Render and draw the slider value text
        slider_text = self.font.render(f"{int(self.slider_value)}", True, (255, 255, 255))
        screen.blit(slider_text, self.text_position)


    def is_over_handle(self, position):
        """
         Check if the given position is over the slider handle

         Parameters
         ----------
         pos( : )tuple) : The position to check

         Returns
         -------
         bool : True if the position is over the slider handle, False otherwise
         """
        # Check if the given position is over the slider handle
        handle_center = (self.slider_position[0] + int((self.slider_value - self.min_value) / (self.max_value - self.min_value) * self.slider_width), self.slider_position[1] + 5)

        # Calculate the distance between the position and handle center
        distance_squared = (position[0] - handle_center[0])**2 + (position[1] - handle_center[1])**2

        # Check if the distance is within the handle radius squared
        return distance_squared <= self.handle_radius**2

    def update_value(self, position):
        """
        Update the slider value based on the mouse position

        Parameters
        ----------
        pos(tuple) : The mouse position

        Returns
        -------
        None
        """
        # Update the slider value based on the mouse position
        if self.dragging:
            # Calculate the mouse position of the mouse within the slider
            mouse_x = position[0] - self.slider_position[0]
            # Update the value within the range of min_value and max_value
            self.slider_value = max(self.min_value, min(self.max_value, mouse_x / self.slider_width * (self.max_value - self.min_value) + self.min_value))

    def reset(self):
        """
        Reset the slider value to its initial value

        Parameters
        -------

        Returns
        -------
        None
        """
        # Reset the slider value to its initial value
        self.slider_value = self.initial_value

    def handle_event(self, event):
        """
        Handle pygame events for the slider

        Parameters
        ----------
        event(pygame.event) : The event to handle

        Returns
        -------
        None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse button is pressed within the slider area
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True  # Start dragging the slider handle

        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging the slider handle when the mouse button is released
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            # If the mouse is moved and the slider handle is being dragged, update the slider value
            if self.dragging:
                self.update()
