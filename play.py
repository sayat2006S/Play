import pygame


pygame.init()
screen = pygame.display.set_mode((600, 600))


maze = [[1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]]

block_size = 50 # размер блока

x = 0
y = 

for row in maze:
    for col in row:
        if col == 1:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, block_size, block_size))
        else:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, block_size, block_size))
        x += block_size
    y += block_size
    x = 0
    
player_pos = [75, 75]
player_size = 25

def draw_player(player_pos):
   pygame.draw.circle(screen, (255, 0, 0), (player_pos[0], player_pos[1]), player_size)
   
def check_move(player_pos):
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         exit()
      
      if event.type == pygame.KEYDOWN:
         x = player_pos[0]
         y = player_pos[1]
         
         if event.key == pygame.K_LEFT:
            x -= player_size
         elif event.key == pygame.K_RIGHT:
            x += player_size
         elif event.key == pygame.K_UP:
            y -= player_size
         elif event.key == pygame.K_DOWN:
            y += player_size
         
         player_pos = [x,y]
      
   return player_pos

def maze_collision(player_pos):
   wall_thickness = 50
   
   for wall in walls:
      if player_pos[1] > wall[1] and player_pos[1] < wall[1] + wall_thickness:
         if player_pos[0] > wall[0] and player_pos[0] < wall[0] + wall_thickness:
            return True
      
   return False

game_over = False

while not game_over:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         exit()
   
   screen.fill((0, 0, 0))
   draw_walls(walls)
   player_pos = check_move(player_pos)
   draw_player(player_pos)
   
   if maze_collision(player_pos):
      game_over = True
   
   pygame.display.update()
   
pygame.quit()
print("Вы прошли игру за {number_of_moves} ходов")