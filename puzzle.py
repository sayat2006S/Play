import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
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
restart_button_rect = pygame.Rect(650, 10, 150, 50)  # Move the restart button to the top-left corner
next_level_button_rect = pygame.Rect(10, 10, 200, 50)

# Interactive objects using Rect
level_objects = [
    {"rect": pygame.Rect(400, 400, 50, 50), "interaction_text": "Click me for a key", "item": "Key"},
    {"rect": pygame.Rect(200, 200, 50, 50), "interaction_text": "Click me for a clue", "item": "Clue"},
    {"rect": pygame.Rect(300, 300, 50, 50), "interaction_text": "Click me for a puzzle piece", "item": "Puzzle Piece"},
    {"rect": pygame.Rect(500, 500, 50, 50), "interaction_text": "Click me for a locked door", "item": None}
]
        
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Key"):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow color for the key
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item
        self.visible = True  # Add a visible attribute

    def interact(self):
        if self.item in inventory:
            inventory.remove(self.item)
            self.visible = False  # Set the visible attribute to False
            return True  # Key was used successfully
        return False  # Key was not used

    def draw(self, screen):
        if self.visible:  # Only draw if the key is visible
            pygame.draw.rect(screen, (255, 255, 0), self.rect)  # Draw the key in yellow
        
class LockedDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Locked Door"):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue color for the locked door
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item
        self.locked = True  # Initialize the door as locked

    def interact(self):
        if self.locked and "Key" in inventory:
            inventory.remove("Key")
            self.locked = False  # Unlock the door
            return True  # Door was opened successfully
        return False  # Door was not opened

    def draw(self, screen):
        if self.locked:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Draw the locked door in blue
        else:
            # Draw the open door or any visual representation for an unlocked door
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
        
# Define classes
class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, interaction_text="", item=None, locked_door=None, is_door=False):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_text = interaction_text
        self.item = item
        self.locked_door = locked_door  # Reference to the locked door
        self.is_door = is_door
        self.visible = True

    def interact(self):
        if self.item:
            inventory.append(self.item)
            show_interaction_text(f"You obtained: {self.item}")
            self.visible = False  # Set visibility to False when picked up

            if self.item == "Key" and self.locked_door:
                # Check if the key is used to open the door
                if "Locked Door" in self.locked_door.item:
                    if self.locked_door.interact():
                        show_interaction_text("You unlocked the door with the key!")

            elif self.item == "Locked Door":
                # Remove the door from the level objects when picked up
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
        self.inventory_objects = pygame.sprite.Group()  # New group for inventory objects

    def setup_level(self):
        self.objects.empty()
        self.inventory_objects.empty()  # Clear the inventory objects group

        # Add code to initialize the level (set up puzzles, objects, etc.)
        if self.level_number == 1:
            key = Key(400, 400)
            self.objects.add(key)
            self.inventory_objects.add(key)  # Add the key to the inventory objects group
            self.objects.add(
                InteractiveObject(200, 200, "Click me for a clue", item="Clue"),
                InteractiveObject(300, 300, "Click me for a puzzle piece", item="Puzzle Piece"),
                LockedDoor(500, 500)
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

    def handle_interaction(self, current_level):
        for obj in self.objects:
            obj.interact()

        # Check for the key in the inventory and open the door
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
    pygame.time.delay(1000)  # Display the text for 2 seconds

def show_victory_screen():
    screen.fill(BLACK)
    victory_text = FONT.render("Victory! Click Next Level to proceed.", True, WHITE)
    screen.blit(victory_text, (WIDTH // 2 - 250, HEIGHT // 2 - 30))

    if current_level < 3:  # Adjust the condition based on the number of levels
        pygame.draw.rect(screen, WHITE, next_level_button_rect)
        next_level_text = FONT.render("Next Level", True, BLACK)
        screen.blit(next_level_text, (WIDTH // 2 - 60, HEIGHT // 2 + 125))

    pygame.draw.rect(screen, WHITE, restart_button_rect)
    restart_text = FONT.render("Restart Level", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - 70, HEIGHT // 2 + 55))

    pygame.display.flip()  # Update the display

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

def show_wrong_solution_screen():
    screen.fill(BLACK)
    wrong_text = FONT.render("Wrong Solution! Restarting Level...", True, WHITE)
    screen.blit(wrong_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the wrong solution screen for 3 seconds
    restart_level()

def show_right_solution_screen():
    screen.fill(BLACK)
    right_text = FONT.render("Congratulations! Proceeding to the Next Level...", True, WHITE)
    screen.blit(right_text, (WIDTH // 2 - 250, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the right solution screen for 3 seconds

    # Logic for moving to the next level
    current_level += 1
    if current_level <= 3:
        level.setup_level()
        inventory = []
        victory_screen = False
    else:
        # Game completed, you may add your completion logic here
        pass

def draw_inventory():
    inventory_surface = pygame.Surface((150, HEIGHT - 20))
    inventory_surface.fill(WHITE)
    screen.blit(inventory_surface, (10, 10))

    inventory_text = FONT.render("Inventory", True, BLACK)
    screen.blit(inventory_text, (20, 20))

    for i, item in enumerate(inventory):
        item_text = FONT.render(f"{i + 1}. {item}", True, BLACK)
        item_rect = item_text.get_rect(topleft=(20, 60 + i * 30))
        screen.blit(item_text, item_rect)

        # Check if the mouse is over the item
        if item_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
                item_rect.x, item_rect.y = pygame.mouse.get_pos()

# Set up groups
all_sprites = pygame.sprite.Group()
interactive_objects = pygame.sprite.Group()

level = Level(current_level)
level.setup_level()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not victory_screen:
                # Check for interactions with objects using Rect
                for obj in level_objects:
                    if obj["rect"].collidepoint(pygame.mouse.get_pos()):
                        if obj["item"] is not None and obj["item"] not in inventory:
                            # Handle interaction logic here
                            inventory.append(obj["item"])
                            show_interaction_text(f"You obtained: {obj['item']}")
                        else:
                            show_interaction_text(obj["interaction_text"])

                        # Additional logic for specific objects
                        if obj["item"] == "Locked Door":
                            if "Key" in inventory:
                                # Open the locked door if the player has the key
                                show_victory_screen()
                                # Additional logic for the locked door if needed
                            else:
                                show_interaction_text("The door is locked. Find a key!")

                # Check for button clicks on the victory screen
                if next_level_button_rect.collidepoint(pygame.mouse.get_pos()):
                    start_new_level()
                elif restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    restart_level()
                    
    all_sprites.update()

    screen.fill(BLACK)
    draw_inventory()
    all_sprites.draw(screen)

    for obj in level.objects:
        obj.draw(screen)

    for obj in level.inventory_objects:
        obj.draw(screen)  # Draw inventory objects

    pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
    restart_text = FONT.render("Restart", True, WHITE)
    screen.blit(restart_text, (restart_button_rect.x + 10, restart_button_rect.y + 10))

    if victory_screen:
        show_victory_screen()

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
