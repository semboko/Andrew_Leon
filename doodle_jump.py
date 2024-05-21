import pygame
from random import randint


pygame.init()
display = pygame.display.set_mode((450, 700))
clock = pygame.time.Clock()

doodler = pygame.image.load("./assets/Doodler.png")
doodler = pygame.transform.scale_by(doodler, 0.3)

platforms = [
    pygame.image.load("./assets/pregular.png"),
    pygame.image.load("./assets/pweak.png"),
    pygame.image.load("./assets/pmoving.png"),
]

platform_coords = []

bottom_y = display.get_height()
for i in range(100):
    x = randint(0, display.get_width())
    y = bottom_y
    ptype = randint(0, 2)
    platform_coords.append([x, y, ptype])
    bottom_y -= randint(50, 80)


dx = 0
dy = 0
vel_y = 0
offset_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        dx -= 8
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        dx += 8

    display.fill((255, 255, 255))
    drect = display.blit(doodler, (dx, dy))

    dy += vel_y
    if vel_y < 15:
        vel_y += .30

    for px, py, ptype in platform_coords:
        pimg = platforms[ptype]
        display.blit(pimg, (px, py))
        prect = pimg.get_rect(left=px, top=py)
        if drect.colliderect(prect) and vel_y > 0:
            vel_y = -10

    pygame.display.update()
    clock.tick(60)

    print(vel_y)
