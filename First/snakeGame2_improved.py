import pygame
from colorNames import *
from pygame.locals import *
import pygameAssets, sys
from pygameAssets import TextBox, Button, InputBox, CheckBox, Slider
from random import randint, randrange

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
FPS = 30
RECT_SIZE = 30
FONT = f'{sys.path[0]}/minecraft.ttf'



class Player(pygame.sprite.Sprite):
    speed = 5
    difficulty = 1
    snake = {}
    length = 0
    size = RECT_SIZE

    boundaries = [(0,0),(SCREEN_WIDTH,SCREEN_HEIGHT)]
    

    def __init__(self):
        super(Player, self).__init__()
        if Player.difficulty == 1:
            Player.speed = 5
        elif Player.difficulty == 2:
            Player.speed = 10
        elif Player.difficulty == 3:
            Player.speed = 15

        self.surf = pygame.Surface((self.size,self.size))
        self.surf.fill((20,200,20))
        self.rect = self.surf.get_rect(
            topleft = (
                (self.size*10) + Player.boundaries[0][0],
                (self.size*10)+ Player.boundaries[0][1]
            )
        )

        self.ishead = False
        self.isFractal = False
        self.waiting = False

        self.direction = None
        self.next_dir = None
        self.pos = None
        
        self.id = self.length
        Player.length += 1

    def __str__(self):
        return self.id.__str__()



    def head(self):
        self.ishead = True
        self.pos = self.rect.topleft
        self.direction = 'up'
        self.next_dir = self.direction
        self.surf.fill((40,160,40))
        Player.snake[self.id] = {'pos':self.pos,'direction':self.direction}
 

    def fractal(self):
        self.isFractal = True
        self.waiting = True

        self.pos = Player.snake[self.id-1]['pos']

        self.direction = Player.snake[self.id-1]['direction']
        self.rect.topleft = self.pos

        Player.snake[self.id] = {'pos':self.pos,'direction':self.direction}

    def onPointUpdate(self):
        if self.ishead:
            for prt in reversed(list(Player.snake.keys())):
                if prt > 0:
                    Player.snake[prt]['direction'] = Player.snake[prt-1]['direction']

            self.direction = self.next_dir
            Player.snake[self.id]['direction'] = self.direction

        if self.waiting and self.isFractal:
            prev = Player.snake[self.id-1]
            diff = (prev['pos'][0] - self.pos[0], prev['pos'][1] - self.pos[1])
            if (prev['pos'][0] - Player.boundaries[0][0]) % self.size == 0 and (prev['pos'][1] - Player.boundaries[0][1]) % self.size == 0:                
                if sum(diff) in [-self.size,self.size]:                    
                    self.waiting = False
    def update(self, pressed_keys = None):
        if self.ishead:
            #Direction update
            if pressed_keys is not None:
                if pressed_keys[K_UP] and self.direction != 'down':
                    self.next_dir = 'up'
                if pressed_keys[K_DOWN] and self.direction != 'up':
                    self.next_dir = 'down'
                if pressed_keys[K_LEFT] and self.direction != 'right':
                    self.next_dir = 'left'
                if pressed_keys[K_RIGHT] and self.direction != 'left':
                    self.next_dir = 'right'


        self.direction = Player.snake[self.id]['direction']
        self.pos = self.rect.topleft

        
        if (self.pos[0] - Player.boundaries[0][0]) % self.size == 0 and (self.pos[1]- Player.boundaries[0][1]) % self.size == 0:
            self.onPointUpdate()

        if not self.waiting:
            if self.direction == 'up':
                self.rect.move_ip(0, -self.speed)
            if self.direction == 'down':        
                self.rect.move_ip(0, self.speed)
            if self.direction == 'left':
                self.rect.move_ip(-self.speed, 0)             
            if self.direction == 'right':
                self.rect.move_ip(self.speed, 0)

        Player.snake[self.id] = {'pos':self.pos,'direction':self.direction}


    def collideWithFood(self,food,food_list):
        if self.rect.colliderect(food.rect):
            food_list.remove(food)
            food.kill()
            return True
    def collideWithSelf(self, fractals):
        for frct in fractals:
            if frct.id > 3:
                if self.rect.colliderect(frct.rect):
                    return True
    def collideWithBorder(self):
        bd = Player.boundaries
        if self.rect.left < bd[0][0] or self.rect.top < bd[0][1] or self.rect.right > bd[1][0] or self.rect.bottom > bd[1][1]:
            return True

    @staticmethod
    def reset():
        Player.snake = {}
        Player.length = 0

class Food(pygame.sprite.Sprite):
    number = 0
    size = RECT_SIZE
    def __init__(self):
        super(Food, self).__init__()
        valid = False
        while not valid:
            x = randrange(self.size,SCREEN_WIDTH-100,self.size) + Player.boundaries[0][0]
            y = randrange(self.size, SCREEN_HEIGHT-100, self.size) + Player.boundaries[0][1]
            valid = True
            for k,v in Player.snake.items():
                if v['pos'][0] == x and v['pos'][1] == y:
                    valid = False

        self.surf = pygame.Surface((self.size,self.size))
        self.surf.fill((180,30,30))
        self.rect = self.surf.get_rect(
            	topleft=(
                    x,
                    y
                )
        ) 
        Food.number += 1    

    @staticmethod
    def reset():
        Food.number = 0
        
        
def kill(sprites):
    for entity in sprites:
        entity.kill()
        
        
        
def createPlayGround():
    size = RECT_SIZE
    height = int(SCREEN_HEIGHT/size)*size
    width = int(SCREEN_WIDTH/size)*size
    
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

        
def menu():
    inMenu = True
        
    TextBox.setScreen(screen)
    Button.setScreen(screen)
    InputBox.setScreen(screen)
    CheckBox.setScreen(screen)
    Slider.setScreen(screen)
    Slider.forceInt(True)


    header = TextBox(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, 'SNAKE!', (255,255,255), fontSize = 100, fontFamily=FONT)
    playButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 200, 50, text='Play!', activeColor=(50,230,50), color=(120,120,120), fontFamily=FONT)

    difficulty1Button = Button(SCREEN_WIDTH/5, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/4, 200, 50, text='Easy', activeColor=(180,40,40), color=(120,120,120), fontFamily=FONT)
    difficulty2Button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/4, 200, 50, text='Normal', activeColor=(180,40,40), color=(120,120,120), fontFamily=FONT)
    difficulty3Button = Button(SCREEN_WIDTH-SCREEN_WIDTH/5, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/4, 200, 50, text='Hard', activeColor=(180,40,40), color=(120,120,120), fontFamily=FONT)

    difficultyButtons = [difficulty1Button, difficulty2Button, difficulty3Button]

    inp = InputBox(SCREEN_WIDTH/2, SCREEN_HEIGHT/8, 200, 50,fontFamily=FONT)
    cb = CheckBox(100, 100, 50)
    slid = Slider(400, 400, 200, pointColor=(255,0,255), activeColor=(200,200,50), min_=5,max_=98)
    
    

    btnPressed = False



    while inMenu:

        if Player.difficulty == 1:
            difficulty1Button.setColor((60,200,60))
        elif Player.difficulty == 2:
            difficulty2Button.setColor((60,200,60))
        elif Player.difficulty == 3:
            difficulty3Button.setColor((60,200,60))

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    inMenu = False
            elif event.type == QUIT:
                inMenu = False
            if playButton.isPressed(event):
                main()

            btnPressed = False
            for btn in difficultyButtons:
                if btn.isPressed(event):
                    btnPressed = True
            if btnPressed:
                difficulty1Button.setColor((120,120,120))
                difficulty2Button.setColor((120,120,120))
                difficulty3Button.setColor((120,120,120))
                if difficulty1Button.isPressed(event):
                    Player.difficulty = 1
                elif difficulty2Button.isPressed(event):
                    Player.difficulty = 2
                elif difficulty3Button.isPressed(event):
                    Player.difficulty = 3

            inp.handle_event(event)
            cb.handle_event(event)
            slid.handle_event(event)
            
        screen.fill((0,0,2))
        header.draw()
        playButton.draw()
        difficulty1Button.draw()
        difficulty2Button.draw()
        difficulty3Button.draw()
        # inp.draw()
        # cb.draw()
        # slid.draw()

        pygame.display.flip()
        
def main():
    
    running = True
    paused = False
    started = False

    Food.reset()
    Player.reset()

    start_length = 3

    pgSurf, pgRect, offset = createPlayGround()

    player = Player()
    player.head()


    new_food = Food()
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(new_food)

    all_food = pygame.sprite.Group()
    all_food.add(new_food)

    fractals = pygame.sprite.Group()


    font = pygame.font.Font(f"{sys.path[0]}/pixel.ttf", 30)
    text = font.render("Score: 0", True, (255, 255, 255))



    startTextBox = TextBox(SCREEN_WIDTH/2, SCREEN_HEIGHT-30, text='- Press space to begin! -', color=(255,255,255), fontSize = 35, fontFamily=FONT)
    scoreTextBox = TextBox(offset[0]+10, offset[1]+10, text=f'Score: 0 | Difficulty: {Player.difficulty} | Speed: {Player.speed}', color=(255,255,255), fontSize=25, fontFamily=FONT,align='topleft',screen=screen)
   
    i = start_length
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #kill(all_sprites)
                    running = False
                elif event.key == K_SPACE:
                    if not started:
                        started = True      
                    else:
                        paused = not paused      
            elif event.type == QUIT:
                running = False
                pygame.quit()
                quit()

        if not paused:
            pressed_keys = pygame.key.get_pressed()

            if started:
                player.update(pressed_keys)
                fractals.update()

            for food in all_food:
                if player.collideWithFood(food, all_food):
                    new_food = Food()
                    new_fractal = Player()
                    new_fractal.fractal()

                    all_sprites.add(new_fractal)
                    all_sprites.add(new_food)
                    all_food.add(new_food)
                    fractals.add(new_fractal)

        
                    scoreTextBox.setText(f'Score: {int(Player.length)-start_length} | Difficulty: {Player.difficulty} | Speed: {Player.speed}')


            if player.collideWithSelf(fractals) or player.collideWithBorder():
                running = False
            
            if i > 1:
                new_frct = Player()
                new_frct.fractal()

                fractals.add(new_frct)
                all_sprites.add(new_frct)
                i -= 1


            screen.fill((255, 255, 255))
            screen.blit(pgSurf, pgRect)

            for entity in all_sprites:
                screen.blit(entity.surf,entity.rect)

            scoreTextBox.draw()

            if not started:
                startTextBox.draw(screen)

            
            pygame.display.flip()












def toggle_fullscreen():
    fscreen = pygame.display.get_surface()
    tmp = fscreen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = fscreen.get_width(),fscreen.get_height()
    flags = fscreen.get_flags()
    bits = fscreen.get_bitsize()
    fscreen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    return fscreen


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Snake Game')
    #toggle_fullscreen()
    menu()