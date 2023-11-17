import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Quest and Puzzle Game")
clock = pygame.time.Clock()

# Game state
current_level = 1
inventory = []

# New game state variables
victory_screen = False
restart_button_rect = pygame.Rect(10, 10, 150, 50)
next_level_button_rect = pygame.Rect(10, 70, 200, 50)

# Mini inventory tab
mini_inventory_rect = pygame.Rect(10, 150, 150, HEIGHT - 170)

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Key"):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow color for the key
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item
        self.visible = True
        self.is_dragging = False  # New attribute to track if the key is being dragged

    def interact(self):
        if self.item in inventory:
            inventory.remove(self.item)
            self.visible = False
            return True  # Key was used successfully
        return False  # Key was not used

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)

    def update(self):
        if self.is_dragging:
            self.rect.center = pygame.mouse.get_pos()

class LockedDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Locked Door"):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue color for the locked door
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item
        self.locked = True

    def interact(self):
        if self.locked and "Key" in inventory:
            inventory.remove("Key")
            self.locked = False
            return True  # Door was opened successfully
        return False  # Door was not opened

    def draw(self, screen):
        if self.locked:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)

class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, interaction_text="", item=None, locked_door=None, is_door=False):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_text = interaction_text
        self.item = item
        self.locked_door = locked_door
        self.is_door = is_door
        self.visible = True
        self.picked_up = False  # New attribute to track if the object has been picked up

    def interact(self):
        if not self.picked_up:  # Check if the object has not been picked up
            if self.item:
                inventory.append(self.item)
                show_interaction_text(f"You obtained: {self.item}")
                self.visible = False
                self.picked_up = True  # Set picked_up to True after picking up the item

                if self.item == "Key" and self.locked_door:
                    if "Locked Door" in self.locked_door.item:
                        if self.locked_door.interact():
                            show_interaction_text("You unlocked the door with the key!")
                elif self.item == "Locked Door":
                    level.objects.remove(self)
            else:
                show_interaction_text(self.interaction_text)

    def draw(self, screen):
        if self.visible:
            if self.is_door:
                pygame.draw.rect(screen, (0, 0, 255), self.rect)
                door_handle_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 20, 10, 10)
                pygame.draw.rect(screen, (255, 255, 0), door_handle_rect)
            else:
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
            self.inventory_objects.add(key)  # Add the key only to the inventory_objects group
            self.objects.add(
                InteractiveObject(200, 200, "Click me for a clue", item="Clue"),
                InteractiveObject(300, 300, "Click me for a puzzle piece", item="Puzzle Piece"),
                LockedDoor(500, 500)
            )

            # Add debug print statements to check if the key is being added to the inventory
            if key in self.inventory_objects:
                print("KEY PICKED UP")
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

    def handle_interaction(self, current_level):
        for obj in self.objects:
            obj.interact()

        if current_level == 1 and "Key" in inventory:
            for obj in self.objects:
                if obj.item == "Locked Door":
                    show_interaction_text("You unlocked the door with the key!")
                    self.objects.remove(obj)
                    show_victory_screen()

def show_interaction_text(text):
    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display the text for 2 seconds

def show_victory_screen():
    screen.fill(BLACK)
    victory_text = FONT.render("Victory! Click Next Level to proceed.", True, WHITE)
    screen.blit(victory_text, (WIDTH // 2 - 250, HEIGHT // 2 - 30))

    if current_level < 3:
        pygame.draw.rect(screen, WHITE, next_level_button_rect)
        next_level_text = FONT.render("Next Level", True, BLACK)
        screen.blit(next_level_text, (WIDTH // 2 - 60, HEIGHT // 2 + 125))

    pygame.draw.rect(screen, WHITE, restart_button_rect)
    restart_text = FONT.render("Restart Level", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - 70, HEIGHT // 2 + 55))

    pygame.display.flip()

def start_new_level():
    global current_level, inventory, victory_screen
    current_level += 1
    inventory = []
    victory_screen = False
    level.setup_level()

def restart_level():
    global current_level, inventory, victory_screen
    current_level = 1
    inventory = []
    victory_screen = False
    level.setup_level()

# Set up groups
all_sprites = pygame.sprite.Group()
interactive_objects = pygame.sprite.Group()

level = Level(current_level)
level.setup_level()

# Game loop
running = True
dragging_key = None  # Variable to keep track of the key being dragged
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not victory_screen:
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
                dragging_key.interact()  # Check for interaction when the key is released
                dragging_key = None

    all_sprites.update()

    screen.fill(BLACK)

    # Draw mini inventory tab
    pygame.draw.rect(screen, WHITE, mini_inventory_rect)
    mini_inventory_text = FONT.render("Inventory", True, BLACK)
    screen.blit(mini_inventory_text, (mini_inventory_rect.x + 10, mini_inventory_rect.y + 10))

    for i, item in enumerate(inventory):
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

    if victory_screen:
        show_victory_screen()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
