import pygame
import random
from pygame.locals import(
  K_SPACE,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)
from pygame.sprite import Group


score=0
gameover = False
SCREEN_W = 600
SCREEN_H = 400
WHITE = (255, 255, 255)
DEAD_BIRD_EVT = pygame.USEREVENT + 1

class Bird(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.isDead = False
    self.surface = pygame.Surface((30, 30))
    self.surface.fill((255, 0, 0))
    self.rect = self.surface.get_rect(
      center=(
        SCREEN_W/2,
        SCREEN_H/2,
      )
    )
    self.speed = 6

  def update(self,pressed_keys):
    global DEAD_BIRD_EVT
    if pressed_keys[K_SPACE]:
      self.rect.move_ip(0, -self.speed)
      self.speed = 6
    else:
      self.rect.move_ip(0, self.speed)
      if self.speed < 20    :
        self.speed = self.speed + 0.24

    if self.rect.bottom > 595 and not self.isDead:
      self.isDead = True
      pygame.event.post(pygame.event.Event(DEAD_BIRD_EVT))


class Pipe(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    # leftside_position = random.randint(SCREEN_W + 20, SCREEN_W + 100)
    leftside_position = SCREEN_W + 50
    bottom_pipe_height = random.randint(100,200)

    self.pipe_bottom = PipeBottom(leftside_position, bottom_pipe_height)
    self.pipe_top = PipeTop(leftside_position, bottom_pipe_height)
    self.add(self.pipe_top)
    self.add(self.pipe_bottom)

    
class PipeTop(pygame.sprite.Sprite):
  def __init__(self,leftside,height):
    super().__init__()
    self.speed = (12)
    self.surface = pygame.Surface((50, SCREEN_H-height-100))
    self.surface.fill((0,250,0))
    self.rect = self.surface.get_rect(topleft=(leftside,0))  

  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill()

class PipeBottom(pygame.sprite.Sprite):
  def __init__(self,leftside,height):
    super().__init__()
    self.speed = (12)
    self.scored = False
    self.surface = pygame.Surface((50, height))
    self.surface.fill((0,250,0))
    self.rect = self.surface.get_rect(bottomleft=(leftside,SCREEN_H))

  def update(self):
    global score
    self.rect.move_ip(-self.speed, 0)
    if self.rect.left <= SCREEN_W/2 and not self.scored:
      score = score + 1
      self.scored = True
    if self.rect.right < 0:
      self.kill()

def GameOver():
  global score, WHITE, screen, gameover

  gameover = True
  pygame.time.set_timer(add_pipe,0)
  bird.kill()
  for pipe in pipes:
    pipe.kill()

  font = pygame.font.SysFont("Arial", 36)
  gameovertxt = font.render("GAME OVER! YOUR SCORE WAS: "+str(score), True, WHITE)
  textRect = gameovertxt.get_rect()
  textRect.center = (SCREEN_W / 2, SCREEN_H / 2)
  screen.blit(gameovertxt,textRect)
  pygame.display.update()

pygame.init()

screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])
add_pipe = pygame.USEREVENT + 0
pygame.time.set_timer(add_pipe,1000)

bird=Bird()
clock = pygame.time.Clock()
pipes =pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(bird)

g_run = True
while g_run:
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        g_run = False

    elif event.type == QUIT:
      g_run = False

    elif event.type == add_pipe:
      new_pipe = Pipe()
      pipes.add(new_pipe)
      all_sprites.add(new_pipe)
    elif event.type == DEAD_BIRD_EVT:
      GameOver()

  if not gameover:
    pressed_keys = pygame.key.get_pressed()
    bird.update(pressed_keys)
    pipes.update()

    screen.fill((0,0,0))
    for entity in all_sprites:
      screen.blit(entity.surface, entity.rect)
      
      if hasattr(entity,'surface2'):
        screen.blit(entity.surface2, entity.rect2)
    
    if pygame.sprite.spritecollideany(bird,pipes):
      pygame.event.post(pygame.event.Event(DEAD_BIRD_EVT))

  pygame.display.flip()
  clock.tick(30)

pygame.quit()