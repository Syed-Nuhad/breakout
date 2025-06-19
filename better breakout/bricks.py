import pygame
import random

BRICK_COLORS = [
    (255, 255, 255),       # Normal
    (0, 255, 0),       # Paddle size up
    (0, 255, 255),     # Multi-ball
    (255, 255, 0),     # Extra life
    (255, 105, 180)    # Speed ball
]

# Types for special bricks
POWERUP_TYPES = {
    1: 'paddle',
    2: 'multi',
    3: 'life',
    4: 'speed'
}

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_type=0, width=75, height=30):
        super().__init__()
        self.brick_type = brick_type  # 0 = normal
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        color = BRICK_COLORS[brick_type]
        pygame.draw.rect(self.image, color, (0, 0, width, height), border_radius=8)
        self.rect = self.image.get_rect(topleft=(x, y))

class BrickWall:
    def __init__(self, rows=6, cols=10, gap=5, offset=60):
        self.rows = rows
        self.cols = cols
        self.gap = gap
        self.offset = offset
        self.brick_group = pygame.sprite.Group()
        self.create_wall()

    def create_wall(self):
        self.brick_group.empty()
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * (75 + self.gap) + self.gap
                y = row * (30 + self.gap) + self.offset
                brick_type = 0

                # Every few bricks add powerups randomly
                if random.random() < 0.15:
                    brick_type = random.randint(1, len(POWERUP_TYPES))

                brick = Brick(x, y, brick_type)
                self.brick_group.add(brick)

    def draw(self, surface):
        self.brick_group.draw(surface)