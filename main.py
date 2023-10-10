import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

screen_height=600
screen_width=600

screen=pygame.display.set_mode([screen_width,screen_height])


# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

game_running = True 
while game_running:
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        game_running = False

    elif event.type == QUIT:
      game_running = False
  

  screen.fill((255, 255, 255))
  surf = pygame.Surface((50, 50))
  surf.fill((0, 0, 0))
  rect = surf.get_rect()
  surf_center = (
    (screen_width-surf.get_width())/2,
    (screen_height-surf.get_height())/2
    )
  screen.blit(surf, surf_center)
  pygame.display.flip()

pygame.quit()
