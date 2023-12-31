import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

door_texture = pygame.image.load("door_texture.png")  # Replace with the actual file path
key_texture = pygame.image.load("key_texture.png")
lock_texture = pygame.image.load("lock_texture.png")

background_image = pygame.image.load("room.png")  # Replace with the actual file path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

class GameState:
    def __init__(self):
        self.current_level = 1
        self.inventory = []
        self.all_levels_completed = False

game_state = GameState()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Квест игра")
clock = pygame.time.Clock()
screen.blit(background_image, (0, 0))
mini_inventory_rect = pygame.Rect(10, 50, 130, 200)

class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, interaction_text="", item=None):
        super().__init__()
        texture = key_texture if item else pygame.image.load("default_texture.png").convert_alpha()
        self.image = pygame.transform.scale(texture, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_text = interaction_text
        self.item = item
        self.visible = True
        self.picked_up = False
    def interact(self):
        if not self.picked_up:
            if self.item:
                game_state.inventory.append(self.item)
                show_interaction_text(f"Вы подобрали: {self.item}")
                self.visible = False
                self.picked_up = True
                if self.item == "Key":
                    show_interaction_text(self.interaction_text)
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.objects = pygame.sprite.Group()
        self.inventory_objects = pygame.sprite.Group()
        self.lock_screen = CombinationLockScreen(None)

    def setup_level(self):
        self.objects.empty()
        self.inventory_objects.empty()

        if self.level_number == 1:
            key_item = "Key1"
            key = Door(300, 145, item=key_item)
            self.inventory_objects.add(key)
            self.objects.add(
                InteractiveObject(150, 500, item=key_item)
            )
        elif self.level_number == 2:
            combination_lock = CombinationLock(400, 400, combination="1234")
            self.objects.add(combination_lock)
            self.lock_screen.combination_lock = combination_lock
            note = Note(350, 170, combination_lock)
            self.objects.add(note)
            self.lock_screen.combination_lock = combination_lock
            plank = SlidingPlank(350, 170)
            self.objects.add(plank)
        elif self.level_number == 3:
            puzzle = PuzzleObject(750, 200)
            self.objects.add(puzzle)
            text_display = TextDisplayObject(220, 100, "Стены хранят секреты")
            level.objects.add(text_display)
            interactive_objects.add(text_display)
        if game_state.current_level == 1 and "Key" in game_state.inventory:
            for obj in self.objects:
                if obj.item == "Locked Door":
                    show_interaction_text("You unlocked the door with the key!")
                    self.objects.remove(obj)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, item="Key"):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("door_texture.png").convert_alpha(), (220, 300))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item
        self.visible = True
        self.is_dragging = False

    def interact(self):
        if self.item in game_state.inventory:
            game_state.inventory.remove(self.item)
            self.visible = False

            if all(obj.picked_up for obj in level.objects if isinstance(obj, InteractiveObject) and obj.item == "Key"):
                show_interaction_text("Уровень пройден")

            return True
        return False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def update(self):
        if self.is_dragging:
            self.rect.center = pygame.mouse.get_pos()
            
class CombinationLock(pygame.sprite.Sprite):
    def __init__(self, x, y, combination="1234"):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("lock_texture.png").convert_alpha(), (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.combination = combination
        self.input_combination = ""
        self.locked = True

    def interact(self, digit):
        if self.locked:
            self.input_combination += str(digit)

            if len(self.input_combination) == len(self.combination):
                if self.input_combination == self.combination:
                    self.unlock_door()
                    show_interaction_text("Дверь открыта")  # Show the correct interaction text
                    return True  # Indicate that the interaction was successful

                self.input_combination = ""
                
        return False  # Indicate that the interaction was unsuccessful

    def unlock_door(self):
        self.locked = False
        show_interaction_text("Дверь открыта")

        # Check if all required objects are picked up to complete the level
        if all(obj.picked_up for obj in level.objects if isinstance(obj, InteractiveObject) and obj.item == "Key"):
            global level_completed  # Declare level_completed as global
            level_completed = True

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
class CombinationLockScreen:
    def __init__(self, combination_lock):
        self.combination_lock = combination_lock
        self.input_combination = ""
        self.is_open = False
        self.popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
        self.close_button_rect = pygame.Rect(self.popup_rect.x + self.popup_rect.width - 30,
                                             self.popup_rect.y, 30, 30)

    def open_lock_screen(self):
        self.is_open = True
        self.input_combination = ""

    def close_lock_screen(self):
        self.is_open = False

    def input_digit(self, digit):
        if self.is_open:
            self.input_combination += str(digit)
            if len(self.input_combination) == len(self.combination_lock.combination):
                if self.input_combination == self.combination_lock.combination:
                    self.combination_lock.unlock_door()
                else:
                    self.close_lock_screen()
                    show_interaction_text("Код неккоректный. Повторите снова.")

    def draw(self, screen):
        if self.is_open:
            pygame.draw.rect(screen, WHITE, self.popup_rect)

            pygame.draw.rect(screen, (255, 0, 0), self.close_button_rect)
            close_text = FONT.render("X", True, BLACK)
            screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y + 5))

            input_text = FONT.render("Введите код:", True, BLACK)
            screen.blit(input_text, (self.popup_rect.x + 20, self.popup_rect.y + 20))

            combination_text = FONT.render(self.input_combination, True, BLACK)
            combination_rect = combination_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(combination_text, combination_rect)
            
class PuzzleObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.colors = [(150, 150, 0), (128, 128, 0), (80, 80, 0), (60, 60, 0), (40, 40, 0)]  
        self.image_index = 0
        self.image = pygame.Surface((8, 8))
        self.image.fill(self.colors[self.image_index])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.click_count = 0
        self.max_clicks = len(self.colors)
        self.completed = False

    def interact(self):
        if not self.completed:
            self.click_count += 1
            if self.click_count < self.max_clicks:
                self.image_index = self.click_count
                self.image.fill(self.colors[self.image_index])
                '''show_interaction_text(f"Clicked {self.click_count} times on the puzzle.")'''
            elif self.click_count == self.max_clicks:
                self.completed = True
                show_interaction_text("Открыт проход, сзади :)")
                global level_completed  
                level_completed = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.colors[self.image_index], self.rect)
        
class SlidingPlank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((120, 50))
        self.image.fill((139, 69, 19))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        self.is_sliding = False
        self.starting_x = x
        self.sliding_distance = 100  

    def interact(self):
        if not self.is_sliding:
            self.is_sliding = True

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (125, 125, 0), self.rect)

    def update(self):
        if self.is_sliding:
            self.rect.x += 5  
            if self.rect.x - self.starting_x >= self.sliding_distance:
                self.is_sliding = False
                self.rect.x = self.starting_x + self.sliding_distance  
                
class Note(pygame.sprite.Sprite):
    def __init__(self, x, y, combination_lock):
        super().__init__()
        self.image = pygame.Surface((100, 50))  
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.combination_lock = combination_lock
        self.font = pygame.font.Font(None, 24)  

    def interact(self):
        show_interaction_text(f"Note: Combination Lock Code - {self.combination_lock.combination}")

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        note_text = self.font.render(f"Код: {self.combination_lock.combination}", True, (0, 0, 0))  # Black text
        text_rect = note_text.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(note_text, text_rect)
        
class TextDisplayObject(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface((400, 150))
        self.image.fill((0, 150, 0))  # Cyan color for the text-displaying object
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.font_size = 24  # Adjust the font size as needed

    def interact(self):
        show_interaction_text(self.text)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 160, 0), self.rect)

        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, (50, 200, 50))  # Black text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

def show_interaction_text(text):
    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)
    
def show_level_completed_popup():
    if game_state.current_level > max_levels:  
        show_interaction_text("Congratulations! You completed all levels!")
        game_state.all_levels_completed = True
        return "quit"  

    popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, WHITE, popup_rect)

    restart_button_rect = pygame.Rect(popup_rect.x + 50, popup_rect.y + 150, 100, 50)
    next_level_button_rect = pygame.Rect(popup_rect.x + 250, popup_rect.y + 150, 100, 50)

    pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
    pygame.draw.rect(screen, (0, 255, 0), next_level_button_rect)

    restart_text = FONT.render("Restart", True, WHITE)
    next_level_text = FONT.render("Next", True, WHITE)

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
                
def show_victory_screen():
    screen.fill(BLACK)  # Change the background color if needed

    victory_text = FONT.render("Вы прошли все уровни!", True, WHITE)
    text_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(victory_text, text_rect)

    pygame.display.flip()

    pygame.time.delay(3000) 

    return "quit" 

all_sprites = pygame.sprite.Group()
interactive_objects = pygame.sprite.Group()

level = Level(game_state.current_level)
level.setup_level()

sliding_plank = SlidingPlank(200, 400)
level.objects.add(sliding_plank)

max_levels = 4 

running = True
dragging_key = None
sliding_plank_clicked = False
level_completed = False
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
            for lock in level.objects:
                if isinstance(lock, CombinationLock) and lock.rect.collidepoint(pygame.mouse.get_pos()):
                    level.lock_screen.open_lock_screen()
            for puzzle in level.objects:
                if isinstance(puzzle, PuzzleObject) and puzzle.rect.collidepoint(pygame.mouse.get_pos()):
                    puzzle.interact()
            for plank in level.objects:
                if isinstance(plank, SlidingPlank) and plank.rect.collidepoint(pygame.mouse.get_pos()):
                    plank.interact()
                    sliding_plank_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_key:
                dragging_key.is_dragging = False
                if dragging_key.interact() and all(obj.picked_up for obj in level.objects if
                                   isinstance(obj, InteractiveObject) and obj.item == "Key"):
                    level_completed = True
            level.lock_screen.close_lock_screen()
        elif event.type == pygame.KEYDOWN:
            if level.lock_screen.is_open:
                if event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    level.lock_screen.input_digit(int(pygame.key.name(event.key)))
                elif event.key == pygame.K_BACKSPACE:
                    level.lock_screen.input_combination = level.lock_screen.input_combination[:-1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_key:
                dragging_key.is_dragging = False
                if dragging_key.interact() and all(obj.picked_up for obj in level.objects if
                                                   isinstance(obj, InteractiveObject) and obj.item == "Key"):
                    level_completed = True
                    
    if game_state.current_level == max_levels and all(obj.picked_up for obj in level.objects if
                                                       isinstance(obj, InteractiveObject) and obj.item == "Key"):
        action = show_victory_screen()
        if action == "quit":
            running = False

    all_sprites.update()

    screen.blit(background_image, (0, 0))  

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
        obj.update()

    for obj in level.inventory_objects:
        obj.draw(screen)
    
    if sliding_plank_clicked:
        if sliding_plank.rect.x - sliding_plank.starting_x >= sliding_plank.sliding_distance:
            sliding_plank_clicked = False

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

    level.lock_screen.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
