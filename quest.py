import pygame
import sys
import time
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LBLUE = (0, 200, 200)
BLACK = (0,0,0)
DARKGREEN = (0, 100, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Quest Game")

player = pygame.Rect(40, 520, PLAYER_SIZE, PLAYER_SIZE)
player_color = WHITE
player_speed = 1

chest = pygame.Rect(150, 530, PLAYER_SIZE, PLAYER_SIZE)
chest_locked = True

chest2 = pygame.Rect(630, 230, PLAYER_SIZE, PLAYER_SIZE)
chest2_locked = True

chest3 = pygame.Rect(450, 122, PLAYER_SIZE, PLAYER_SIZE)
chest3_locked = True

key = pygame.Rect(225, 320, 25, 15)
key_color = (200, 150, 0)
key_picked_up = False

key2 = pygame.Rect(200, 550, 25, 15)
key2_color = (0, 255, 0)
key2_picked_up = False

key3 = pygame.Rect(650, 145, 25, 15)
key3_color = (0, 0, 255)
key3_picked_up = False

npc_size = 30
npc = pygame.Rect(400, 300, npc_size, npc_size)
npc_color = (255, 0, 0)
npc_speed = 0.5  # Adjust this to control the NPC's speed

message_display_duration = 2 
message_start_time = 0  

obstacles = [pygame.Rect(100, 100, 20, 600),
    pygame.Rect(300, 100, 400, 20),
    pygame.Rect(100, 500, 400, 20),
    pygame.Rect(680, 100, 20, 420),
    pygame.Rect(180, 100, 20, 300),
    pygame.Rect(260, 320, 20, 40),
    pygame.Rect(500, 300, 20, 100),
    pygame.Rect(500, 100, 20, 100),
    pygame.Rect(600, 360, 20, 100),
    pygame.Rect(500, 280, 100, 20),
    pygame.Rect(420, 165, 100, 20),
    pygame.Rect(420, 180, 20, 100),
    pygame.Rect(600, 200, 20, 100),
    pygame.Rect(600, 400, 20, 100),
    pygame.Rect(560, 400, 45, 20),
    pygame.Rect(600, 200, 100, 20),
    pygame.Rect(200, 100, 20, 300),
    pygame.Rect(180, 250, 100, 20),
    pygame.Rect(325, 250, 45, 20),
    pygame.Rect(500, 200, 45, 20),
    pygame.Rect(180, 10, 40, 100),
    pygame.Rect(600, 500, 100, 20),
    pygame.Rect(500, 500, 100, 20),
    pygame.Rect(350, 250, 20, 100),
    pygame.Rect(200, 350, 200, 50),
    pygame.Rect(350, 300, 20, 100),
    pygame.Rect(350, 100, 20, 100),
    pygame.Rect(440, 260, 10, 20),
    pygame.Rect(515, 180, 30, 20),
    #pygame.Rect(500, 470, 20, 40),
    pygame.Rect(610, 280, 30, 20),
    pygame.Rect(240, 440, 160, 20),
    pygame.Rect(240, 450, 20, 70),
    pygame.Rect(180, 380, 20, 80),
    pygame.Rect(440, 450, 20, 70),
    pygame.Rect(0, 0, SCREEN_WIDTH, 20),
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
    pygame.Rect(0, 0, 20, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),]
surroundings = [pygame.Rect(0, 0, 800, 800)]

exit_rect = pygame.Rect(40, 520, PLAYER_SIZE, PLAYER_SIZE)
exit_color = GREEN
exit_unlocked = False

quests = [
    {"description": "Unlock all chests", "completed": False},
]

font = pygame.font.Font(None, 36)

def check_quest_completion():
    if not chest_locked and not chest2_locked and not chest3_locked:
        quests[0]["completed"] = True

game_over = False
running = True
while running and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

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

    new_player_rect = pygame.Rect(new_x, new_y, PLAYER_SIZE, PLAYER_SIZE)

    collision = False
    for obstacle in obstacles:
        if new_player_rect.colliderect(obstacle):
            collision = True
            if obstacle == key and not key_picked_up:
                collision = True
            elif obstacle == key2 and not key2_picked_up:
                collision = True
            elif obstacle == key3 and not key3_picked_up:
                collision = True
            elif obstacle == chest and chest_locked:
                collision = True
            elif obstacle == chest2 and chest2_locked:
                collision = True
            elif obstacle == chest3 and chest3_locked:
                collision = True
            break
        
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            game_over = True

    if not collision:
        player.x = new_x
        player.y = new_y

    screen.fill((0, 0, 0))

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
    
    if npc.x < player.x:
        npc.x += npc_speed
    elif npc.x > player.x:
        npc.x -+ npc_speed

    if npc.y < player.y:
        npc.y += npc_speed
    elif npc.y > player.y:
        npc.y -+ npc_speed

    # Check if NPC touches the player
    if player.colliderect(npc):
        game_over = True
    
    if game_over:
        screen.fill(RED)  # You can change this color or add an image for the game over screen
        game_over_text = "Game Over! Press Q to Quit"
        text_surface = font.render(game_over_text, True, WHITE)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        pygame.display.update()

    for surrounding in surroundings:
        pygame.draw.rect(screen, BLACK, surrounding)

    for obstacle in obstacles:
        pygame.draw.rect(screen, LBLUE, obstacle)

    pygame.draw.rect(screen, player_color, player)

    if key and not key_picked_up:
        pygame.draw.rect(screen, key_color, key)

    if key and player.colliderect(key) and not key_picked_up:
        key_picked_up = True
        key = None
        message_start_time = time.time()

    if key2 and not key2_picked_up:
        pygame.draw.rect(screen, key2_color, key2)

    if key2 and player.colliderect(key2) and not key2_picked_up:
        key2_picked_up = True
        key2 = None
        message_start_time = time.time()

    if key3 and not key3_picked_up:
        pygame.draw.rect(screen, key3_color, key3)

    if key3 and player.colliderect(key3) and not key3_picked_up:
        key3_picked_up = True
        key3 = None
        message_start_time = time.time()
    
    if message_start_time > 0:
        current_time = time.time()
        if current_time - message_start_time < message_display_duration:
            message_text = "Picked up key"
            text_surface = font.render(message_text, True, WHITE)
            screen.blit(text_surface, (20, 100))
        else:
            message_start_time = 0

    if player.colliderect(chest) and chest_locked:
        if key_picked_up:
            chest_locked = False
            check_quest_completion()
        else:
            locked_text = "Chest is locked. Find the ORANGE key to unlock it."
            text_surface = font.render(locked_text, True, WHITE)
            screen.blit(text_surface, (20, 60))

    if player.colliderect(chest2) and chest2_locked:
        if key2_picked_up:
            chest2_locked = False
            check_quest_completion()
        else:
            locked_text = "Chest is locked. Find the GREEN key to unlock it."
            text_surface = font.render(locked_text, True, WHITE)
            screen.blit(text_surface, (20, 60))

    if player.colliderect(chest3) and chest3_locked:
        if key3_picked_up:
            chest3_locked = False
            check_quest_completion()
        else:
            locked_text = "Chest is locked. Find the BLUE key to unlock it."
            text_surface = font.render(locked_text, True, WHITE)
            screen.blit(text_surface, (20, 60))


    if not chest_locked:
        pygame.draw.rect(screen, key_color, chest)
    else:
        pygame.draw.rect(screen, RED, chest)
        
    if not chest2_locked:
        pygame.draw.rect(screen, key2_color, chest2)
    else:
        pygame.draw.rect(screen, RED, chest2)

    if not chest3_locked:
        pygame.draw.rect(screen, key3_color, chest3)
    else:
        pygame.draw.rect(screen, RED, chest3)
        
    if all([not chest_locked, not chest2_locked, not chest3_locked]):
        exit_unlocked = True

    # Draw the exit if it's unlocked
    if exit_unlocked:
        pygame.draw.rect(screen, exit_color, exit_rect)

        # Check if the player collides with the exit
        if player.colliderect(exit_rect):
            print("Congratulations! You completed the game!")
            running = False  # You can customize this part based on your game's requirements
        
    pygame.draw.rect(screen, npc_color, npc)

    if not quests[0]["completed"]:
        quest_text = "Quest: " + ("Completed" if all([not chest_locked, not chest2_locked, not chest3_locked]) else "Unlock all chests")
    else:
        quest_text = "Quest: Completed"
    text_surface = font.render(quest_text, True, WHITE)
    screen.blit(text_surface, (20, 20))
    
    while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False

    pygame.display.update()

pygame.quit()
sys.exit()
