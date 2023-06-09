import pygame
from random import randint


pygame.init()
size = 500, 500
display = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

class Particle:
    radius = 5
    color = (0, 0, 0)
    
    def __init__(self, x, y):
        self.coords = x, y
        self.velocity_y = 4
        self.velocity_x = randint(-5, 5)
        self.lifetime = 255
    
    def update_position(self):
        x, y = self.coords
        self.coords = x + self.velocity_x, y + self.velocity_y
        self.velocity_y = self.velocity_y * 1.04
        self.lifetime = self.lifetime - 7
    
    def draw(self):
        c = 255 - abs(self.lifetime)
        pygame.draw.circle(display, (c, c, c), self.coords, self.radius)


particles = set()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pk = pygame.key.get_pressed()
    if pk[pygame.K_SPACE] or pk[pygame.K_w]:
        p = Particle(250, 50)
        particles.add(p)

    display.fill((255, 255, 255))
    
    particles_to_remove = set()
    for p in particles:
        p.update_position()
        p.draw()
        if p.lifetime <= 0:
            particles_to_remove.add(p)
            
    for p in particles_to_remove:
        particles.remove(p)
        print(p)
    
    pygame.display.update()
    clock.tick(fps)
