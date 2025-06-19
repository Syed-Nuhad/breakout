import pygame

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.width = 120
        self.height = 15
        self.color = (255, 255, 255)
        self.speed = 7
        # Start paddle near bottom center
        self.rect = pygame.Rect(screen_width // 2 - self.width // 2, screen_height - 40, self.width, self.height)

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)