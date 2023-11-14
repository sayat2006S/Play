import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SOLUTION_RECT = pygame.Rect(300, 200, 5, 5)  # Coordinates of the hidden solution
SOLUTION_COLOR = (255, 0, 0)  # Green color for the solution

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle Game")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if SOLUTION_RECT.collidepoint(mouse_x, mouse_y):
                print("Congratulations! You found the solution.")
                pygame.quit()
                sys.exit()

    screen.fill((255, 255, 255)) 
    pygame.draw.rect(screen, SOLUTION_COLOR, SOLUTION_RECT)  

    pygame.display.flip()

    pygame.time.Clock().tick(60)
