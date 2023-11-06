import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Quest Game")

player = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)
player_color = WHITE
player_speed = 1

npc = pygame.Rect(400, 300, PLAYER_SIZE, PLAYER_SIZE)
npc_color = RED
npc_speed = 8

obstacles = [pygame.Rect(200, 200, 100, 20), pygame.Rect(600, 400, 20, 150), pygame.Rect(300, 400, 200, 200)]
surroundings = [pygame.Rect(0, 0, 800, 800)]

quests = [{
    'description': 'Defeat the evil monster',
    'completed': False
}]

font = pygame.font.Font(None, 36)

flash_start_time = None
flash_duration = 500
flash_color = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # Check for collision with NPC
    if player.colliderect(npc) and not quests[0]['completed']:
        flash_start_time = pygame.time.get_ticks()
        quests[0]['completed'] = True

    # Handle the white flash effect
    if flash_start_time is not None:
        current_time = pygame.time.get_ticks()
        if current_time - flash_start_time < flash_duration:
            flash_color = WHITE
        else:
            flash_start_time = None
            flash_color = None

    # Move the NPC
    direction = random.choice(['left', 'right', 'up', 'down'])
    if direction == 'left':
        npc.x -= npc_speed
    elif direction == 'right':
        npc.x += npc_speed
    elif direction == 'up':
        npc.y -= npc_speed
    elif direction == 'down':
        npc.y += npc_speed

    # Keep the NPC within the screen boundaries
    npc.x = max(0, min(npc.x, SCREEN_WIDTH - PLAYER_SIZE))
    npc.y = max(0, min(npc.y, SCREEN_HEIGHT - PLAYER_SIZE))

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            # If there's a collision, adjust the player's position to avoid the obstacle
            if keys[pygame.K_LEFT]:
                player.x = obstacle.right
            if keys[pygame.K_RIGHT]:
                player.x = obstacle.left - PLAYER_SIZE
            if keys[pygame.K_UP]:
                player.y = obstacle.bottom
            if keys[pygame.K_DOWN]:
                player.y = obstacle.top - PLAYER_SIZE

    screen.fill((0, 0, 0))  # Clear the screen

    # Draw surroundings
    for surrounding in surroundings:
        pygame.draw.rect(screen, DARKGREEN, surrounding)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, obstacle)

    if flash_color is not None:
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash_surface.fill(flash_color)
        screen.blit(flash_surface, (0, 0))

    if not quests[0]['completed']:
        pygame.draw.rect(screen, npc_color, npc)  # Draw the NPC

    pygame.draw.rect(screen, player_color, player)  # Draw the player

    # Display quest status
    quest_text = "Quest: " + ("Completed" if quests[0]['completed'] else "Defeat the evil monster")
    text_surface = font.render(quest_text, True, WHITE)
    screen.blit(text_surface, (20, 20))

    pygame.display.update()

pygame.quit()
sys.exit()
