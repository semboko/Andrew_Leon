import pygame


pygame.init()
display = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    pygame.display.update()
    clock.tick(60)
