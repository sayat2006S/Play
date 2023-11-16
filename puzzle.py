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

# Define classes
class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, interaction_text, item=None, locked_door=None):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_text = interaction_text
        self.item = item
        self.locked_door = locked_door  # Reference to the locked door

    def interact(self):
        if self.item:
            inventory.append(self.item)
            show_interaction_text(f"You obtained: {self.item}")
            if self.item == "Key":
                # Check if the key is used to open the door
                if self.locked_door and "Locked Door" in self.locked_door.item:
                    level.objects.remove(self.locked_door)
                    show_interaction_text("You unlocked the door with the key!")
                    show_victory_screen()
        elif self.interaction_text == "Click me for a locked door":
            if "Key" in inventory:
                show_interaction_text("You unlocked the door with the key!")
                level.objects.remove(self.locked_door)
            else:
                show_interaction_text("The door is locked. Find a key!")
        else:
            show_interaction_text(self.interaction_text)

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.objects = pygame.sprite.Group()

    def setup_level(self):
        self.objects.empty()

        # Add code to initialize the level (set up puzzles, objects, etc.)
        if self.level_number == 1:
            locked_door = InteractiveObject(500, 500, "Click me for a locked door", item="Locked Door")
            self.objects.add(
                InteractiveObject(400, 400, "Click me for a key", item="Key", locked_door=locked_door),
                InteractiveObject(200, 200, "Click me for a clue", item="Clue"),
                InteractiveObject(300, 300, "Click me for a puzzle piece", item="Puzzle Piece"),
                locked_door
            )
        elif self.level_number == 2:
            locked_door = InteractiveObject(500, 500, "Click me for a locked door", item="Locked Door")
            self.objects.add(
                InteractiveObject(100, 100, "Click me for the next clue", item="Next Clue"),
                InteractiveObject(200, 200, "Click me for a map", item="Map"),
                InteractiveObject(300, 300, "Click me for a keycard", item="Keycard")
            )
        elif self.level_number == 3:
            locked_door = InteractiveObject(500, 500, "Click me for a locked door", item="Locked Door")
            self.objects.add(
                InteractiveObject(100, 100, "Click me for the final puzzle piece", item="Final Puzzle Piece"),
                InteractiveObject(200, 200, "Click me for the exit key", item="Exit Key"),
                InteractiveObject(300, 300, "Click me for the secret code", item="Secret Code")
            )

    def handle_interaction(self, current_level):
        for obj in self.objects:
            if obj.rect.collidepoint(pygame.mouse.get_pos()):
                obj.interact()
                if current_level == 3 and len(inventory) == 3:
                    show_right_solution_screen()
                else:
                    show_wrong_solution_screen()

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
        screen.blit(item_text, (20, 60 + i * 30))

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
        if obj.item == "Locked Door":
            pygame.draw.rect(screen, (0, 0, 255), obj.rect)  # Draw the locked door in blue
        else:
            pygame.draw.rect(screen, WHITE, obj.rect)  # Draw other objects in white

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
