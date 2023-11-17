import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize font
FONT = pygame.font.Font(None, 36)

# Game state
class GameState:
    def __init__(self):
        self.current_level = 1
        self.inventory = []

game_state = GameState()

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Quest and Puzzle Game")
clock = pygame.time.Clock()

level_completed = False

# New game state variables
restart_button_rect = pygame.Rect(10, 10, 150, 50)

# Mini inventory tab
mini_inventory_rect = pygame.Rect(10, 150, 150, HEIGHT - 170)

class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, interaction_text="", item=None):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_text = interaction_text
        self.item = item
        self.visible = True
        self.picked_up = False

    def interact(self):
        if not self.picked_up:
            if self.item:
                game_state.inventory.append(self.item)
                show_interaction_text(f"You obtained: {self.item}")
                self.visible = False
                self.picked_up = True
                if self.item == "Key":
                    show_interaction_text(self.interaction_text)

    def draw(self, screen):
        if self.visible:
            if self.item:
                pygame.draw.rect(screen, WHITE, self.rect)

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.objects = pygame.sprite.Group()
        self.inventory_objects = pygame.sprite.Group()

    def setup_level(self):
        self.objects.empty()
        self.inventory_objects.empty()

        if self.level_number == 1:
            key = Door(400, 400)
            self.inventory_objects.add(key)
            self.objects.add(
                InteractiveObject(600, 500, item="Key")
            )
        elif self.level_number == 2:
            key = Door(400, 400)
            self.inventory_objects.add(key)
            self.objects.add(
                InteractiveObject(600, 500, item="Key")
            )
        elif self.level_number == 3:
            key = Door(400, 400)
            self.inventory_objects.add(key)
            self.objects.add(
                InteractiveObject(600, 500, item="Key")
            )
        if game_state.current_level == 1 and "Key" in game_state.inventory:
            for obj in self.objects:
                if obj.item == "Locked Door":
                    show_interaction_text("You unlocked the door with the key!")
                    self.objects.remove(obj)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Key"):
        super().__init__()
        self.image = pygame.Surface((100, 200))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(400, 100))
        self.item = item
        self.visible = True
        self.is_dragging = False

    def interact(self):
        if self.item in game_state.inventory:
            game_state.inventory.remove(self.item)
            self.visible = False

            # Check for victory condition
            if all(obj.picked_up for obj in level.objects if isinstance(obj, InteractiveObject) and obj.item == "Key"):
                show_interaction_text("You completed the level!")

            return True
        return False

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)

    def update(self):
        if self.is_dragging:
            self.rect.center = pygame.mouse.get_pos()

def show_interaction_text(text):
    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)
    
def show_level_completed_popup():
    popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, WHITE, popup_rect)

    restart_button_rect = pygame.Rect(popup_rect.x + 50, popup_rect.y + 150, 150, 50)
    next_level_button_rect = pygame.Rect(popup_rect.x + 250, popup_rect.y + 150, 150, 50)

    pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
    pygame.draw.rect(screen, (0, 255, 0), next_level_button_rect)

    restart_text = FONT.render("Restart", True, WHITE)
    next_level_text = FONT.render("Next Level", True, WHITE)

    screen.blit(restart_text, (restart_button_rect.x + 10, restart_button_rect.y + 10))
    screen.blit(next_level_text, (next_level_button_rect.x + 10, next_level_button_rect.y + 10))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return "restart"
                elif next_level_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return "next_level"

# Set up groups
all_sprites = pygame.sprite.Group()
interactive_objects = pygame.sprite.Group()

level = Level(game_state.current_level)
level.setup_level()

# Game loop
running = True
dragging_key = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for obj in level.objects:
                if isinstance(obj, InteractiveObject) and obj.rect.collidepoint(pygame.mouse.get_pos()):
                    obj.interact()
            for key in level.inventory_objects:
                if isinstance(key, Door) and key.rect.collidepoint(pygame.mouse.get_pos()):
                    key.is_dragging = True
                    dragging_key = key
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_key:
                dragging_key.is_dragging = False
                if dragging_key.interact() and all(obj.picked_up for obj in level.objects if
                                                   isinstance(obj, InteractiveObject) and obj.item == "Key"):
                    level_completed = True

    all_sprites.update()

    screen.fill(BLACK)

    # Draw mini inventory tab
    pygame.draw.rect(screen, WHITE, mini_inventory_rect)
    mini_inventory_text = FONT.render("Inventory", True, BLACK)
    screen.blit(mini_inventory_text, (mini_inventory_rect.x + 10, mini_inventory_rect.y + 10))

    for i, item in enumerate(game_state.inventory):
        item_text = FONT.render(f"{i + 1}. {item}", True, BLACK)
        item_rect = item_text.get_rect(
            topleft=(mini_inventory_rect.x + 10, mini_inventory_rect.y + 40 + i * 30))
        screen.blit(item_text, item_rect)

    all_sprites.draw(screen)

    for obj in level.objects:
        obj.draw(screen)

    for obj in level.inventory_objects:
        obj.draw(screen)

    pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
    restart_text = FONT.render("Restart", True, WHITE)
    screen.blit(restart_text, (restart_button_rect.x + 10, restart_button_rect.y + 10))

    if level_completed:
        action = show_level_completed_popup()
        if action == "restart":
            game_state = GameState()
            level = Level(game_state.current_level)
            level.setup_level()
            level_completed = False
        elif action == "next_level":
            game_state.current_level += 1
            level = Level(game_state.current_level)
            level.setup_level()
            level_completed = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
