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

# Define classes
class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, interaction_text, item=None):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.interaction_text = interaction_text
        self.item = item

    def interact(self):
        if self.item:
            inventory.append(self.item)
            show_interaction_text(f"You obtained: {self.item}")
        else:
            show_interaction_text(self.interaction_text)

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.objects = pygame.sprite.Group()

    def setup_level(self):
        # Clear existing objects
        self.objects.empty()

        # Add code to initialize the level (set up puzzles, objects, etc.)
        if self.level_number == 1:
            # Level 1 setup
            obj1 = InteractiveObject(100, 100, "Click me for a key", item="Key")
            obj2 = InteractiveObject(200, 200, "Click me for a clue", item="Clue")
            obj3 = InteractiveObject(300, 300, "Click me for a puzzle piece", item="Puzzle Piece")

            self.objects.add(obj1, obj2, obj3)
        elif self.level_number == 2:
            # Level 2 setup
            obj4 = InteractiveObject(100, 100, "Click me for the next clue", item="Next Clue")
            obj5 = InteractiveObject(200, 200, "Click me for a map", item="Map")
            obj6 = InteractiveObject(300, 300, "Click me for a keycard", item="Keycard")

            self.objects.add(obj4, obj5, obj6)
        elif self.level_number == 3:
            # Level 3 setup
            obj7 = InteractiveObject(100, 100, "Click me for the final puzzle piece", item="Final Puzzle Piece")
            obj8 = InteractiveObject(200, 200, "Click me for the exit key", item="Exit Key")
            obj9 = InteractiveObject(300, 300, "Click me for the secret code", item="Secret Code")

            self.objects.add(obj7, obj8, obj9)

    def handle_interaction(self, current_level):
        # Add code to handle interactions with objects in the level
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
    pygame.time.delay(2000)  # Display the text for 2 seconds

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
    start_new_level()

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

# Game loop
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for mouse clicks on interactive objects
            level.handle_interaction(current_level)

    # Update
    all_sprites.update()

    # Draw / Render
    screen.fill(BLACK)

    # Draw inventory bar
    draw_inventory()

    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
