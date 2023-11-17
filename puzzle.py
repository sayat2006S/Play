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
        self.victory_screen = False


game_state = GameState()

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Quest and Puzzle Game")
clock = pygame.time.Clock()

# New game state variables
restart_button_rect = pygame.Rect(10, 10, 150, 50)
next_level_button_rect = pygame.Rect(10, 70, 200, 50)

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
                    show_interaction_text("You unlocked a secret passage with the key!")
            else:
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
            key = Key(400, 400)
            self.inventory_objects.add(key)
            self.objects.add(
                InteractiveObject(200, 200, "Click me for a clue", item="Clue"),
                InteractiveObject(300, 300, "Click me for a puzzle piece", item="Puzzle Piece"),
                InteractiveObject(500, 500, "Click me for the secret passage key", item="Key")
            )
        elif self.level_number == 2:
            self.objects.add(
                InteractiveObject(100, 100, "Click me for the next clue", item="Next Clue"),
                InteractiveObject(200, 200, "Click me for a map", item="Map"),
                InteractiveObject(300, 300, "Click me for a keycard", item="Keycard")
            )
        elif self.level_number == 3:
            self.objects.add(
                InteractiveObject(100, 100, "Click me for the final puzzle piece", item="Final Puzzle Piece"),
                InteractiveObject(200, 200, "Click me for the exit key", item="Exit Key"),
                InteractiveObject(300, 300, "Click me for the secret code", item="Secret Code")
            )

        if game_state.current_level == 1 and "Key" in game_state.inventory:
            for obj in self.objects:
                if obj.item == "Locked Door":
                    show_interaction_text("You unlocked the door with the key!")
                    self.objects.remove(obj)
                    show_victory_screen()

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Key"):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item
        self.visible = True
        self.is_dragging = False

    def interact(self):
        if self.item in game_state.inventory:
            game_state.inventory.remove(self.item)
            self.visible = False
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
    pygame.time.delay(2000)

def show_victory_screen():
    screen.fill(BLACK)
    victory_text = FONT.render("Victory! Click Next Level to proceed.", True, WHITE)
    screen.blit(victory_text, (WIDTH // 2 - 250, HEIGHT // 2 - 30))

    if game_state.current_level < 3:
        pygame.draw.rect(screen, WHITE, next_level_button_rect)
        next_level_text = FONT.render("Next Level", True, BLACK)
        screen.blit(next_level_text, (WIDTH // 2 - 60, HEIGHT // 2 + 125))

    pygame.draw.rect(screen, WHITE, restart_button_rect)
    restart_text = FONT.render("Restart Level", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - 70, HEIGHT // 2 + 55))

    pygame.display.flip()

def start_new_level():
    game_state.current_level += 1
    game_state.inventory = []
    game_state.victory_screen = False
    level.setup_level()

def restart_level():
    game_state.current_level = 1
    game_state.inventory = []
    game_state.victory_screen = False
    level.setup_level()

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
            if not game_state.victory_screen:
                for obj in level.objects:
                    if isinstance(obj, InteractiveObject) and obj.rect.collidepoint(pygame.mouse.get_pos()):
                        obj.interact()
                for key in level.inventory_objects:
                    if isinstance(key, Key) and key.rect.collidepoint(pygame.mouse.get_pos()):
                        key.is_dragging = True
                        dragging_key = key
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_key:
                dragging_key.is_dragging = False
                dragging_key.interact()
                dragging_key = None

    all_sprites.update()

    screen.fill(BLACK)

    # Draw mini inventory tab
    pygame.draw.rect(screen, WHITE, mini_inventory_rect)
    mini_inventory_text = FONT.render("Inventory", True, BLACK)
    screen.blit(mini_inventory_text, (mini_inventory_rect.x + 10, mini_inventory_rect.y + 10))

    for i, item in enumerate(game_state.inventory):
        item_text = FONT.render(f"{i + 1}. {item}", True, BLACK)
        item_rect = item_text.get_rect(topleft=(mini_inventory_rect.x + 10, mini_inventory_rect.y + 40 + i * 30))
        screen.blit(item_text, item_rect)

    all_sprites.draw(screen)

    for obj in level.objects:
        obj.draw(screen)

    for obj in level.inventory_objects:
        obj.draw(screen)

    pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
    restart_text = FONT.render("Restart", True, WHITE)
    screen.blit(restart_text, (restart_button_rect.x + 10, restart_button_rect.y + 10))

    if game_state.victory_screen:
        show_victory_screen()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
