import pygame
import sys
import time
import math
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
DOOM_GRAY = (64, 64, 64)
DOOM_RED = (255, 0, 0)
DOOM_GREEN = (0, 255, 0)
DOOM_BLUE = (0, 0, 255)
DOOM_YELLOW = (255, 255, 0)
DOOM_BROWN = (139, 69, 19)
DOOM_DARKGRAY = (32, 32, 32)
DOOM_BLACK = (0, 0, 0)
DOOM_WHITE = (255, 255, 255)
DARKGREEN = (0, 100, 0)
player_color = DOOM_WHITE
key_color = DOOM_YELLOW
key2_color = DOOM_GREEN
key3_color = DOOM_BLUE
exit_color = DOOM_GREEN
LBLUE = DOOM_DARKGRAY
RED = DOOM_RED
GREEN = DOOM_GREEN
BLACK = DOOM_BLACK
WHITE = DOOM_WHITE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Quest Game")

reverse_controls = False
timer_enabled = True
elapsed_time = 0
turret_enabled = True

cover_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
cover_color = DOOM_BLACK
show_cover = False

def generate_random_coordinates(enabled=True, exclude_rects=[], obstacles=[]):
    if not enabled:
        return 0, 0  # Return a fixed position (you can modify this as needed)
    
    while True:
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        new_rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

        # Check if the new coordinates collide with any obstacles or existing items
        if not any(new_rect.colliderect(rect) for rect in exclude_rects + obstacles):
            return x, y

def start_menu():
    menu_font = pygame.font.Font(None, 48)
    title_text = menu_font.render("2D Quest Game", True, WHITE)
    play_text = menu_font.render("Play", True, WHITE)

    screen.fill(BLACK)
    pygame.draw.rect(screen, LBLUE, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 40, 120, 50))  # Play button background
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(play_text, (SCREEN_WIDTH // 2 - 35, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 40, 120, 50)
                if play_button_rect.collidepoint(mouse_x, mouse_y):
                    waiting_for_input = False

player = pygame.Rect(40, 520, PLAYER_SIZE, PLAYER_SIZE)
player_color = WHITE
player_speed = 1
player_health = 200
MAX_PLAYER_HEALTH = 200
player_health = MAX_PLAYER_HEALTH  # Set the initial player health to the maximum value

class Turret:
    def __init__(self, x, y):
        self.x = 430
        self.y = 330
        self.width = 40
        self.height = 40
        self.color = DOOM_GRAY
        self.rotation_speed = 0.1  # Adjust the rotation speed as needed
        self.projectiles = []
        self.shoot_delay = 600  # Adjust the delay between shots as needed
        self.last_shot_time = 0
        self.rotation = 0  # Initialize the rotation attribute
        self.enabled = True  

    def rotate(self):
        if self.enabled:
            self.rotation += self.rotation_speed
            if self.rotation >= 360:
                self.rotation -= 360

    def shoot(self):
        if self.enabled and pygame.time.get_ticks() - self.last_shot_time > self.shoot_delay:
            projectile = Projectile(self.x + self.width / 2, self.y + self.height / 2, self.rotation)
            self.projectiles.append(projectile)
            self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        if self.enabled:
            self.rotate()
            self.shoot()
        
    def reset(self):
        self.x = 400
        self.y = 300
        self.projectiles = []
        self.last_shot_time = 0
        self.rotation = 0

class Projectile:
    def __init__(self, x, y, rotation):
        self.x = x
        self.y = y
        self.speed = 0.2  # Adjust the projectile speed as needed
        self.rotation = rotation

    def update(self):
        # Move the projectile in the direction of its rotation
        self.x += self.speed * math.cos(math.radians(self.rotation))
        self.y -= self.speed * math.sin(math.radians(self.rotation))

chest = pygame.Rect(*generate_random_coordinates(), PLAYER_SIZE, PLAYER_SIZE)
chest_locked = True

chest2 = pygame.Rect(*generate_random_coordinates(), PLAYER_SIZE, PLAYER_SIZE)
chest2_locked = True

chest3 = pygame.Rect(*generate_random_coordinates(), PLAYER_SIZE, PLAYER_SIZE)
chest3_locked = True

key = pygame.Rect(*generate_random_coordinates(), 25, 15)
key_color = (200, 150, 0)
key_picked_up = False

key2 = pygame.Rect(*generate_random_coordinates(), 25, 15)
key2_color = (0, 255, 0)
key2_picked_up = False

key3 = pygame.Rect(*generate_random_coordinates(), 25, 15)
key3_color = (0, 0, 255)
key3_picked_up = False

turret = Turret(400, 300)

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
    pygame.Rect(180, 10, 20, 100),
    pygame.Rect(600, 500, 100, 20),
    pygame.Rect(500, 500, 100, 20),
    pygame.Rect(350, 250, 20, 100),
    pygame.Rect(200, 350, 200, 20),
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

def show_health_bar():
    health_bar_rect = pygame.Rect(590, SCREEN_HEIGHT - 15, player_health, 20)
    pygame.draw.rect(screen, DARKGREEN, health_bar_rect)

def decrease_health(amount):
    global player_health
    player_health = max(0, player_health - amount)

def increase_health(amount):
    global player_health
    player_health = min(MAX_PLAYER_HEALTH, player_health + amount)

def check_quest_completion():
    if not chest_locked and not chest2_locked and not chest3_locked:
        quests[0]["completed"] = True
        
def reset_game():
    global player, player_color, player_speed, chest, chest2, chest3, chest_locked, chest2_locked, chest3_locked, player_health
    global key, key_color, key_picked_up, key2, key2_color, key2_picked_up, key3, key3_color, key3_picked_up
    global exit_unlocked, elapsed_time, show_cover
    
    turret.reset()

    # Reset player position and status
    player = pygame.Rect(40, 520, PLAYER_SIZE, PLAYER_SIZE)
    player_color = WHITE
    player_speed = 1
    player_health = MAX_PLAYER_HEALTH

    # Reset chest and key status
    chest = pygame.Rect(*generate_random_coordinates(), PLAYER_SIZE, PLAYER_SIZE)
    chest_locked = True
    key = pygame.Rect(*generate_random_coordinates(), 25, 15)
    key_color = (200, 150, 0)
    key_picked_up = False

    chest2 = pygame.Rect(*generate_random_coordinates(), PLAYER_SIZE, PLAYER_SIZE)
    chest2_locked = True
    key2 = pygame.Rect(*generate_random_coordinates([key]), 25, 15)
    key2_color = (0, 255, 0)
    key2_picked_up = False

    chest3 = pygame.Rect(*generate_random_coordinates(), PLAYER_SIZE, PLAYER_SIZE)
    chest3_locked = True
    key3 = pygame.Rect(*generate_random_coordinates([key, key2]), 25, 15)
    key3_color = (0, 0, 255)
    key3_picked_up = False

    # Reset exit status
    exit_unlocked = False

    quests[0]["completed"] = False
    
    show_cover = show_cover  # Maintain the show_cover state

    # Draw the cover if show_cover is True
    if show_cover:
        pygame.draw.rect(screen, cover_color, cover_rect)
    else:
        show_cover = False
    
    elapsed_time = 0
    
def show_victory_screen(finish_time):
    victory_font = pygame.font.Font(None, 48)
    victory_text = victory_font.render("Congratulations! You Completed the Game!", True, WHITE)
    restart_text = victory_font.render("Press R to Restart or Q to Quit", True, WHITE)
    
    if timer_enabled:  # Only display finish time if the timer is enabled
        finish_time_text = victory_font.render(f"Finish Time: {int(finish_time)} seconds", True, WHITE)
        screen.blit(finish_time_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50))

    screen.fill(GREEN)  # Customize the background color for the victory screen
    screen.blit(victory_text, (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 - 100))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    reset_game()  # Reset the game state
                    waiting_for_input = False
                    start_menu()  # Display the start menu
        
start_menu()

finish_time = 0
victory_screen_displayed = False
running = True
show_start_menu = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if show_start_menu:
        start_menu()
        show_start_menu = False
        
    if timer_enabled:
        elapsed_time += pygame.time.get_ticks() / 1000

    keys = pygame.key.get_pressed()

    new_x = player.x
    new_y = player.y

    if reverse_controls:
        if keys[pygame.K_LEFT]:
            new_x += player_speed
        if keys[pygame.K_RIGHT]:
            new_x -= player_speed
        if keys[pygame.K_UP]:
            new_y += player_speed
        if keys[pygame.K_DOWN]:
            new_y -= player_speed
    else:
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

    for surrounding in surroundings:
        pygame.draw.rect(screen, BLACK, surrounding)

    for obstacle in obstacles:
        pygame.draw.rect(screen, LBLUE, obstacle)
        
    if show_cover:
        pygame.draw.rect(screen, cover_color, cover_rect)

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
            show_victory_screen(finish_time)
            reset_game()
            show_start_menu = True
        finish_time = elapsed_time


    if not quests[0]["completed"]:
        quest_text = "Quest: " + ("Completed" if all([not chest_locked, not chest2_locked, not chest3_locked]) else "Grab 3 keys and unlock all chests")
    else:
        quest_text = "Quest: Completed"
    text_surface = font.render(quest_text, True, WHITE)
    screen.blit(text_surface, (20, 20))
    
    show_health_bar()
    
    if turret_enabled:
        turret.update()
        for projectile in turret.projectiles:
            projectile.update()
            pygame.draw.rect(screen, DOOM_WHITE, (projectile.x, projectile.y, 5, 5))  # Adjust projectile size as needed

        pygame.draw.rect(screen, turret.color, (turret.x, turret.y, turret.width, turret.height))
        pygame.draw.line(screen, DOOM_WHITE, (turret.x + turret.width / 2, turret.y + turret.height / 2),
                        (turret.x + turret.width / 2 + 30 * math.cos(math.radians(turret.rotation)),
                        turret.y + turret.height / 2 - 30 * math.sin(math.radians(turret.rotation))))

        # Check for collisions with the player and handle health decrement
        for projectile in turret.projectiles:
            projectile_rect = pygame.Rect(projectile.x, projectile.y, 5, 5)
            if player.colliderect(projectile_rect):
                decrease_health(50)
                turret.projectiles.remove(projectile)
                if player_health <= 0:
                    reset_game()  # Reset the game state
                    start_menu()  # Display the start menu
                    
    if all([not chest_locked, not chest2_locked, not chest3_locked]):
        show_cover = False
                
    if timer_enabled:
        timer_font = pygame.font.Font(None, 24)
        timer_text = timer_font.render(f"Timer: {int(elapsed_time)} seconds", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 20))
    
    if not victory_screen_displayed:
        pygame.display.update()
    else:
        show_victory_screen()
        victory_screen_displayed = False

    while victory_screen_displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                victory_screen_displayed = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    victory_screen_displayed = False
                elif event.key == pygame.K_r:
                    reset_game()
                    victory_screen_displayed = False
                    start_menu()  # You may want to add a function to display a start menu
            
    pygame.display.update()
    
if finish_time > 0:
    show_victory_screen(finish_time)

pygame.quit()
sys.exit()
