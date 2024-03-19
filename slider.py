import pygame

class Slider:
    def __init__(self, position, width, min_value, max_value, initial_value):
        self.position = position
        self.width = width
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.handle_radius = 10  # Adjust as needed
        self.dragging = False

    def draw(self, screen):
        # Calculate the slider's position and size
        slider_rect = pygame.Rect(self.position[0], self.position[1], self.width, 10)
        handle_center = (self.position[0] + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width), self.position[1] + 5)

        # Draw the slider track
        pygame.draw.rect(screen, (200, 200, 200), slider_rect)

        # Draw the handle
        pygame.draw.circle(screen, (100, 100, 100), handle_center, self.handle_radius)

    def is_over_handle(self, pos):
        handle_center = (self.position[0] + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width), self.position[1] + 5)
        distance_squared = (pos[0] - handle_center[0])**2 + (pos[1] - handle_center[1])**2
        return distance_squared <= self.handle_radius**2

    def update_value(self, pos):
        if self.dragging:
            # Calculate new value based on mouse position
            relative_x = pos[0] - self.position[0]
            self.value = max(self.min_value, min(self.max_value, relative_x / self.width * (self.max_value - self.min_value) + self.min_value))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update()