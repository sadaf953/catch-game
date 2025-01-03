import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")
clock = pygame.time.Clock()

# Basket properties
basket_width = 100
basket_height = 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 40
basket_speed = 10

# Falling object properties
object_width = 20
object_height = 20
objects = []

# Bomb properties
bombs = []

# Game variables
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Function to create a new object or bomb
def create_falling_item(is_bomb=False):
    x = random.randint(0, WIDTH - object_width)
    y = -object_height
    color = RED if is_bomb else BLUE
    return {"x": x, "y": y, "color": color, "is_bomb": is_bomb}

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # Create new objects and bombs periodically
    if random.randint(1, 30) == 1:
        objects.append(create_falling_item())
    if random.randint(1, 50) == 1:
        bombs.append(create_falling_item(is_bomb=True))

    # Update objects and check for collisions
    for obj in objects[:]:
        obj["y"] += 5
        if obj["y"] > HEIGHT:
            objects.remove(obj)
        elif basket_x < obj["x"] < basket_x + basket_width and basket_y < obj["y"] < basket_y + basket_height:
            objects.remove(obj)
            score += 1

    # Update bombs and check for collisions
    for bomb in bombs[:]:
        bomb["y"] += 5
        if bomb["y"] > HEIGHT:
            bombs.remove(bomb)
        elif basket_x < bomb["x"] < basket_x + basket_width and basket_y < bomb["y"] < basket_y + basket_height:
            bombs.remove(bomb)
            lives -= 1
            if lives == 0:
                running = False

    # Draw basket
    pygame.draw.rect(screen, BLACK, (basket_x, basket_y, basket_width, basket_height))

    # Draw objects
    for obj in objects:
        pygame.draw.rect(screen, obj["color"], (obj["x"], obj["y"], object_width, object_height))

    # Draw bombs
    for bomb in bombs:
        pygame.draw.rect(screen, bomb["color"], (bomb["x"], bomb["y"], object_width, object_height))

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Game over screen
screen.fill(WHITE)
game_over_text = font.render("Game Over!", True, RED)
final_score_text = font.render(f"Your Score: {score}", True, BLACK)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 10))
pygame.display.flip()
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
sys.exit()
