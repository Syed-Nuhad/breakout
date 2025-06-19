import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 10
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(screen_width // 2, screen_height // 2, self.radius * 2, self.radius * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.last_paddle_collision = False  # Prevent multiple paddle hits
        self.last_wall_collision = False     # Prevent multiple wall hits

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_wall_collision(self):
        collided = False
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.speed_x *= -1
            collided = True
        if self.rect.top <= 0:
            self.speed_y *= -1
            collided = True
        return collided

    def check_paddle_collision(self, paddle_rect):
        if self.rect.colliderect(paddle_rect):
            if not self.last_paddle_collision:
                self.speed_y *= -1
                self.last_paddle_collision = True
                return True  # Sound should play
        else:
            self.last_paddle_collision = False
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)