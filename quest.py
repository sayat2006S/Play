import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)
YELLOW = (255, 255, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Quest Game")

player = pygame.Rect(40, 520, PLAYER_SIZE, PLAYER_SIZE)
player_color = WHITE
player_speed = 1

# Define a chest and a key
chest = pygame.Rect(150, 530, PLAYER_SIZE, PLAYER_SIZE)
chest_locked = True

# Define the key color and draw it
key = pygame.Rect(250, 400, 30, 15)
key_color = (200, 150, 0)
key_picked_up = False

obstacles = [pygame.Rect(100, 100, 20, 600),
    pygame.Rect(300, 100, 400, 20),
    pygame.Rect(100, 500, 400, 20),
    pygame.Rect(680, 100, 20, 420),
    pygame.Rect(180, 100, 20, 300),
    pygame.Rect(500, 100, 20, 100),
    pygame.Rect(500, 400, 100, 20),
    pygame.Rect(600, 400, 20, 100),
    pygame.Rect(600, 200, 100, 20),
    pygame.Rect(200, 100, 20, 300),
    pygame.Rect(200, 200, 100, 20),
    pygame.Rect(180, 10, 40, 100),
    pygame.Rect(600, 500, 100, 20),
    pygame.Rect(500, 500, 100, 20),
    pygame.Rect(350, 250, 20, 100),
    pygame.Rect(200, 350, 200, 30),
    pygame.Rect(350, 300, 20, 100),
    pygame.Rect(350, 100, 20, 100),
    pygame.Rect(200, 450, 200, 50),
    pygame.Rect(0, 0, SCREEN_WIDTH, 20),
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
    pygame.Rect(0, 0, 20, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),]
surroundings = [pygame.Rect(0, 0, 800, 800)]

quests = [{"description": "Open chest", "completed": False}]

font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Calculate the new position based on player's input
    new_x = player.x
    new_y = player.y

    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed

    # Create a new Rect representing the player's potential new position
    new_player_rect = pygame.Rect(new_x, new_y, PLAYER_SIZE, PLAYER_SIZE)

    # Check for collisions with obstacles
    collision = False
    for obstacle in obstacles:
        if new_player_rect.colliderect(obstacle):
            collision = True
            break

    # Only update the player's position if there's no collision
    if not collision:
        player.x = new_x
        player.y = new_y

    screen.fill((0, 0, 0))

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            if keys[pygame.K_LEFT]:
                player.x = obstacle.right
            if keys[pygame.K_RIGHT]:
                player.x = obstacle.left - PLAYER_SIZE
            if keys[pygame.K_UP]:
                player.y = obstacle.bottom
            if keys[pygame.K_DOWN]:
                player.y = obstacle.top - PLAYER_SIZE

    screen.fill((0, 0, 0))

    # Draw surroundings
    for surrounding in surroundings:
        pygame.draw.rect(screen, DARKGREEN, surrounding)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, obstacle)

    pygame.draw.rect(screen, player_color, player)

    if key and not key_picked_up:
        pygame.draw.rect(screen, key_color, key)

    # Check for collision with the key
    if key and player.colliderect(key) and not key_picked_up:
        # If the player collides with the key and it hasn't been picked up,
        # pick up the key and remove it from the screen
        key_picked_up = True
        key = None

    # Check for collision with the locked chest
    if player.colliderect(chest) and chest_locked:
        if key_picked_up:
            # If the player has picked up the key, unlock the chest
            chest_locked = False
        else:
            # If the player doesn't have the key, display a message
            locked_text = "Chest is locked. Find the key to unlock it."
            text_surface = font.render(locked_text, True, WHITE)
            screen.blit(text_surface, (20, 60))

    # Draw the chest
    if not chest_locked:
        pygame.draw.rect(screen, YELLOW, chest)
    else:
        pygame.draw.rect(screen, RED, chest)

    # Display the quest status with the chest information
    if not quests[0]["completed"]:
        quest_text = "Quest: " + ("Completed" if not chest_locked else "Open chest")
    else:
        quest_text = "Quest: Completed"
    text_surface = font.render(quest_text, True, WHITE)
    screen.blit(text_surface, (20, 20))

    pygame.display.update()

pygame.quit()
sys.exit()
