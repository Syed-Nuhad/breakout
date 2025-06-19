import pygame
import random
from bricks import BrickWall
from ball import Ball

pygame.init()
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("git.WAV")

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Clock & font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 15)
paddle_speed = 7

# Ball
ball = Ball(WIDTH, HEIGHT)
ball_active = False  # Only starts moving after pressing SPACE

# Brick wall
wall = BrickWall()

# Game variables
score = 0
level = 1
show_level_msg = True
level_timer = 0
lives = 3
paused = False

# Power-ups
powerups = []
powerup_timer = 0
powerup_active = False

# Fix ball starting speed to something reasonable
ball.speed_x = 4
ball.speed_y = -4

# Main loop
running = True
while running:
    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_active:
                ball_active = True
            if event.key == pygame.K_p:
                paused = not paused

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Keep ball aligned to paddle before game starts
    if not ball_active:
        ball.rect.centerx = paddle.centerx
        ball.rect.bottom = paddle.top - 1  # Just above paddle

    if not paused and ball_active:
        ball.move()
        ball.check_wall_collision()
        ball.check_paddle_collision(paddle)

        # Play hit sound only when ball hits paddle or bricks (avoid spamming)
        # For that, let's check paddle collision separately and play once only if colliding:
        if ball.rect.colliderect(paddle):
            hit_sound.play()

        # Brick collision
        hit_brick = None
        for brick in wall.brick_group:
            if ball.rect.colliderect(brick.rect):
                hit_brick = brick
                break

        if hit_brick:
            wall.brick_group.remove(hit_brick)
            ball.speed_y *= -1
            score += 10
            hit_sound.play()

            if random.random() < 0.2:
                powerup = pygame.Rect(hit_brick.rect.centerx, hit_brick.rect.centery, 20, 20)
                powerups.append(powerup)

            if len(wall.brick_group) == 0:
                level += 1
                show_level_msg = True
                ball.speed_x *= 1.1
                ball.speed_y *= 1.1
                wall.create_wall()

        if ball.rect.bottom > HEIGHT:
            lives -= 1
            if lives <= 0:
                running = False
            else:
                ball_active = False
                ball = Ball(WIDTH, HEIGHT)
                ball.speed_x = 4 * (-1 if random.random() < 0.5 else 1)
                ball.speed_y = -4
                paddle.width = 120
                paddle = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
                powerup_active = False

    # Power-up movement
    for powerup in powerups[:]:
        powerup.y += 4
        if powerup.colliderect(paddle):
            paddle.width = min(paddle.width + 40, WIDTH)
            paddle = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            powerups.remove(powerup)
            powerup_active = True
            powerup_timer = 300
        elif powerup.top > HEIGHT:
            powerups.remove(powerup)

    if powerup_active:
        powerup_timer -= 1
        if powerup_timer <= 0:
            paddle.width = 120
            paddle = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            powerup_active = False

    # Drawing
    screen.fill(BLACK)
    wall.draw(screen)
    pygame.draw.rect(screen, WHITE, paddle)
    ball.draw(screen)
    for powerup in powerups:
        pygame.draw.rect(screen, CYAN, powerup, border_radius=5)

    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    if show_level_msg:
        msg = font.render(f"Level {level}", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        level_timer += 1
        if level_timer > 120:
            show_level_msg = False
            level_timer = 0

    if paused:
        pause_text = font.render("Game Paused - Press P to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

pygame.quit()