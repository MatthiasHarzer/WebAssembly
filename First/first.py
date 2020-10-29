'''Cool Game'''
import pygame
from pygame.locals import *
from pygameAssets import *
from colorNames import *
from random import randint, randrange

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
FPS = 30
RECT_SIZE = 30

class Player(pygame.sprite.Sprite):
    speed = 8
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((RECT_SIZE,RECT_SIZE))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(
            center = (
                int((SCREEN_WIDTH-self.surf.get_width())/2),
                int((SCREEN_HEIGHT-self.surf.get_height())/2)
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT    

# class Enemy(pygame.sprite.Sprite):
#     def __init__(self):
#         super(Enemy, self).__init__()
        

#     def update(self):
#         pass

def createPlayGround():
    size = RECT_SIZE
    height = SCREEN_HEIGHT
    width = SCREEN_WIDTH
    
    xOffset = int((SCREEN_WIDTH-width)/2)
    yOffset = int((SCREEN_HEIGHT-height)/2)

    
    Player.boundaries = [(xOffset,yOffset), (SCREEN_WIDTH-xOffset,SCREEN_HEIGHT-yOffset)]
    surf = pygame.Surface((SCREEN_WIDTH-(xOffset*2),SCREEN_HEIGHT-(yOffset*2)))
    surf.fill((102,102,102))
    rect = surf.get_rect(
        topleft=(
            xOffset,
            yOffset
        )
    )
    return surf, rect, (xOffset,yOffset)

def game():
    running = True

    pgSurf, pgRect, offset = createPlayGround()
    
    player = Player()
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        pressed_keys = pygame.key.get_pressed()
        
        player.update(pressed_keys)

        screen.fill((255, 255, 255))
        screen.blit(pgSurf, pgRect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            pass
        
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Cool Game');
    game()