import pygame

pygame.init()

display = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
fps = 60


class Pacman:
    def __init__(self, x, y):
        # self.x = x
        # self.y = y
        self.pos = pygame.Vector2(x, y)
        
        self.angle = 0
        
        self.velocity = pygame.Vector2(0, 0)
        
        raw_image = pygame.image.load("assets/pacman.png")
        self.image = pygame.transform.scale(raw_image, (50, 50))
    
    def handle_key(self, key: int):
        if key == pygame.K_UP:
            self.velocity = pygame.Vector2(0, -5)
            self.angle = 90
        
        if key == pygame.K_DOWN:
            self.velocity = pygame.Vector2(0, 5)
            self.angle = 270
        
        if key == pygame.K_LEFT:
            self.velocity = pygame.Vector2(-5, 0)
            self.angle = 180
        
        if key == pygame.K_RIGHT:
            self.velocity = pygame.Vector2(5, 0)
            self.angle = 0
            
    def step(self):
        self.pos += self.velocity
        
        self.pos.x %= display.get_width()
        self.pos.y %= display.get_height()
        
    
    def handle_pressed_keys(self, pressed):
        if pressed[pygame.K_UP]:
            if self.y - 25 < 0:
                self.y = display.get_height() - 25
                return
            self.y -= 5
            self.angle = 90
        if pressed[pygame.K_DOWN]:
            if self.y + 25 > display.get_height():
                self.y = 25
                return
            self.y += 5
            self.angle = 270
        if pressed[pygame.K_LEFT]:
            if self.x - 25 < 0:
                self.x = display.get_width() - 25
                return
            self.x -= 5
            self.angle = 180
        if pressed[pygame.K_RIGHT]:
            if self.x + 25 > display.get_width():
                self.x = 25
                return
            self.x += 5
            self.angle = 0
        
    def draw(self):
        w = self.image.get_width()
        h = self.image.get_height()
        
        # position = (self.x - w/2, self.y - h/2)
        position = self.pos - pygame.Vector2(w/2, h/2)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        display.blit(rotated_image, position)

pacman = Pacman(350, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            pacman.handle_key(event.key)
    
    # pressed = pygame.key.get_pressed()
    # pacman.handle_pressed_keys(pressed)
    
    pacman.step()
              
    display.fill((10, 10, 10))
    
    pacman.draw()
    
    pygame.display.update()
    clock.tick(fps)
                


    