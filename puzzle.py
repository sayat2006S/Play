import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_LEVELS = 3  # Number of levels
current_level = 1
transition_time = 2000  # 2000 milliseconds (2 seconds) for transition

def generate_solution():
    return pygame.Rect(random.randint(100, 700), random.randint(100, 500), 20, 20)

def generate_solution_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def fade(surface, width, height, alpha):
    fade_surface = pygame.Surface((width, height))
    fade_surface.set_alpha(alpha)
    fade_surface.fill((0, 0, 0))
    surface.blit(fade_surface, (0, 0))

SOLUTION_RECT = generate_solution()
SOLUTION_COLOR = generate_solution_color()

# Define murder mystery clues for Level 1
murder_location = pygame.Rect(200, 400, 50, 50)
wrong_solution = pygame.Rect(600, 400, 50, 50)  # Wrong solution

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Murder Mystery - Level {}".format(current_level))

clock = pygame.time.Clock()
transition_start_time = 0

def draw_transition_circle(radius):
    pygame.draw.circle(screen, (255, 255, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), radius)

def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over - Correct Solution Clicked", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the game over message for 3 seconds
    pygame.quit()
    sys.exit()

def transition_to_next_level():
    global current_level, SOLUTION_RECT, SOLUTION_COLOR

    current_level += 1
    if current_level <= MAX_LEVELS:
        SOLUTION_RECT = generate_solution()
        SOLUTION_COLOR = generate_solution_color()
        pygame.display.set_caption("Murder Mystery - Level {}".format(current_level))
    else:
        print("You've completed all levels. Game Over!")
        pygame.quit()
        sys.exit()

while current_level <= MAX_LEVELS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the player clicked on the correct or wrong solution
            if SOLUTION_RECT.collidepoint(mouse_x, mouse_y):
                game_over()
            elif murder_location.collidepoint(mouse_x, mouse_y):
                print("Congratulations! You found a clue in the murder mystery for Level {}".format(current_level))
                transition_start_time = pygame.time.get_ticks()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, SOLUTION_COLOR, SOLUTION_RECT)

    # Draw murder mystery clues on Level 1
    pygame.draw.rect(screen, (0, 0, 255), murder_location)
    pygame.draw.rect(screen, (0, 255, 0), wrong_solution)  # Display the wrong solution

    if transition_start_time > 0:
        elapsed_time = pygame.time.get_ticks() - transition_start_time
        if elapsed_time < transition_time:
            alpha = 255 - int((elapsed_time / transition_time) * 255)
            fade(screen, SCREEN_WIDTH, SCREEN_HEIGHT, alpha)
        else:
            transition_to_next_level()
            transition_start_time = 0

    pygame.display.flip()
    clock.tick(60)
