import pygame
from random import randint, choices


pygame.init()
display = pygame.display.set_mode((450, 700))
clock = pygame.time.Clock()

doodler = pygame.image.load("./assets/Doodler.png")
doodler = pygame.transform.scale_by(doodler, 0.3)

game_over_img = pygame.image.load("./assets/game_over.png")
# game_over_img = pygame.transform.scale_by(game_over_img, 0.8)

score_font = pygame.font.Font("./assets/Electrolize-Regular.ttf", 30)
# score_font = pygame.font.SysFont("Arial", 30)

platforms = [
    pygame.image.load("./assets/pregular.png"),
    pygame.image.load("./assets/pweak.png"),
    pygame.image.load("./assets/pmoving.png"),
]

spring0 = pygame.image.load("./assets/spring_0.png")

jump_sound = pygame.mixer.Sound("./assets/jumpland.wav")
crack_sound = pygame.mixer.Sound("./assets/multiple_cracks_1.wav")

platform_coords = []
spring_coords = []


bottom_y = display.get_height()


def generate_platform():
    global bottom_y
    x = randint(0, display.get_width() - 70)
    ptype = choices((0, 1, 2), (0.8, 0.09, 0.11))[0]
    platform_coords.append([x, bottom_y, ptype, 1])
    if randint(1, 100) < 8 and ptype == 0:
        spring_x = x + randint(0, 57)
        spring_coords.append([spring_x, bottom_y - 10])

    if ptype == 1:
        bottom_y -= randint(10, 20)
    else:
        bottom_y -= randint(50, 80)


for i in range(10):
    generate_platform()


dx = 200
dy = 400
vel_y = 0
offset_y = 0
score = 0
game_over = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_over is True:
                bottom_y = display.get_height()
                platform_coords = []
                for i in range(10):
                    generate_platform()
                dx = 200
                dy = 400
                vel_y = 0
                offset_y = 0
                score = 0
                game_over = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        dx -= 8
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        dx += 8

    display.fill((255, 255, 255))
    drect = display.blit(doodler, (dx, dy))
    drect.height -= 55
    drect.width -= 20
    drect.top += 55
    # pygame.draw.rect(display, (255, 0, 0), drect, 1)

    offset_y += vel_y
    if vel_y < 15:
        vel_y += .30

    for platform in platform_coords:
        px, py, ptype, direction = platform
        pimg = platforms[ptype]
        prect = display.blit(pimg, (px, py - offset_y))
        # pygame.draw.rect(display, (255, 0, 0), prect, 1)
        if drect.colliderect(prect) and vel_y > 4:
            if ptype == 1:
                platform_coords.remove(platform)
                crack_sound.play()
            else:
                vel_y = -10
                jump_sound.play()
        if ptype == 2:
            platform[0] += direction
        if platform[0] < 0:
            platform[3] = 1
        if platform[0] > 400:
            platform[3] = -1
        if (py - offset_y) > 800:
            platform_coords.remove(platform)

    for s in spring_coords:
        spring_x, spring_y = s
        srect = display.blit(spring0, (spring_x, spring_y - offset_y))
        if drect.colliderect(srect):
            vel_y = -40
        if (spring_y - offset_y) > 800:
            spring_coords.remove(s)

    last_platform = platform_coords[-1]
    if last_platform[1] - offset_y > 0:
        generate_platform()

    if offset_y * -1 > score:
        score = round(offset_y * -1, 1)

    if last_platform[1] < offset_y - 600:
        display.blit(game_over_img, (45, 0))
        game_over = True

    score_img = score_font.render(str(score) + "m", True, (0, 0, 0))
    display.blit(score_img, (0, 0))

    pygame.display.update()
    clock.tick(60)
