import pygame
from random import randint, choice


pygame.init()
display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

bg_img = pygame.image.load("./assets/fj_bg.jpg")
w, h = bg_img.get_size()
scale_factor = 0.7
bg_img = pygame.transform.scale(bg_img, (w * scale_factor, h * scale_factor))

sword_sounds = [
    pygame.mixer.Sound("./assets/sword-1a.wav"),
    pygame.mixer.Sound("./assets/sword-1b.wav"),
    pygame.mixer.Sound("./assets/sword-arm-2a.wav"),
    pygame.mixer.Sound("./assets/sword-arm-2b.wav"),
]

gong_sound = pygame.mixer.Sound("./assets/gong.mp3")

electolize_large = pygame.font.Font("./assets/Electrolize-Regular.ttf", 40)
electolize_xlarge = pygame.font.Font("./assets/Electrolize-Regular.ttf", 70)

explosion_sound = pygame.mixer.Sound("./assets/rumble.flac")
explosion_sound.set_volume(0.8)

explosion_tiles = pygame.image.load("./assets/Tile.png")

score = 0
lives = 3
game_over = False

fruit_imgs = []

half_imgs1 = []
half_imgs2 = []

for fruit_name in ("apple", "banana", "peach", "strawberry", "watermelon"):
    file_name = "./assets/" + fruit_name + ".png"
    img = pygame.image.load(file_name)
    fruit_imgs.append(img)

    half_name1 = "./assets/" + fruit_name + "-1.png"
    half_name2 = "./assets/" + fruit_name + "-2.png"
    half_imgs1.append(pygame.image.load(half_name1))
    half_imgs2.append(pygame.image.load(half_name2))


bomb_image = pygame.image.load("./assets/bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (100, 100))

fruits = []
halves = []
bombs = []
explosions = []


def spawn_fruit():
    kind = randint(0, 4)
    fruit_width = fruit_imgs[kind].get_width()
    x = randint(0, 500 - fruit_width)
    y = randint(-500, -100)
    fruits.append([x, y, kind, 0])


def spawn_bomb():
    x = randint(0, 500 - bomb_image.get_width())
    y = randint(-500, -100)
    bombs.append([x, y, 0])


def spawn_explosion(x, y):
    explosions.append([x, y, 0])


for _ in range(5):
    spawn_fruit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            for fruit in fruits:
                x, y, kind, yvel = fruit
                fi = fruit_imgs[kind]
                fruit_hitbox = pygame.Rect((x, y), fi.get_size())
                if fruit_hitbox.collidepoint(event.pos):
                    fruits.remove(fruit)
                    score += 2
                    choice(sword_sounds).play()
                    halves.append([x, y, half_imgs1[kind], -8, yvel])
                    halves.append([x, y, half_imgs2[kind], 8, yvel])

            for bomb in bombs:
                bomb_hitbox = bomb_image.get_rect(x=bomb[0], y=bomb[1])
                if bomb_hitbox.collidepoint(event.pos):
                    bombs.remove(bomb)
                    lives -= 1
                    explosion_sound.play()
                    spawn_explosion(bomb[0], bomb[1])

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            score = 0
            for _ in range(5):
                spawn_fruit()
            lives = 3
            bombs = []
            fruits = []
            game_over = False

    display.blit(bg_img, (-340, 0))
    for f in fruits:
        img = fruit_imgs[f[2]]
        display.blit(img, (f[0], f[1]))
        if not game_over:
            f[1] = f[1] + f[3]
            f[3] = f[3] + 0.028
        if f[1] > display.get_height():
            lives -= 1
            fruits.remove(f)

    for b in bombs:
        display.blit(bomb_image, (b[0], b[1]))
        if not game_over:
            b[1] = b[1] + b[2]
            b[2] = b[2] + 0.028

    score_img = electolize_large.render(
        "Score: " + str(score), True, (255, 255, 255)
    )
    display.blit(score_img, (0, 0))

    lives_img = electolize_large.render(
        "Lives: " + str(lives), True, (255, 255, 255)
    )
    display.blit(lives_img, (0, 50))

    if randint(0, 45) == 0 and not game_over:
        spawn_fruit()

    if randint(0, 200) == 0 and not game_over:
        print("Spawning a new bomb!")
        spawn_bomb()

    for half in halves:
        x, y, img, xvel, yvel = half
        display.blit(img, (x, y))
        half[0] = half[0] + xvel
        half[3] = half[3] * 0.95

        half[1] = half[1] + yvel
        half[4] = half[4] + 0.028

    for e in explosions:
        row = e[2] // 8
        col = e[2] % 8
        crop_area = pygame.Rect((col * 256, row * 256), (256, 256))
        display.blit(explosion_tiles, (e[0] - 64, e[1] - 64), crop_area)
        e[2] += 1
        if e[2] > 63:
            explosions.remove(e)

    if lives <= 0:
        lives = 3
        game_over = True
        fruits = []
        bombs = []
        gong_sound.play()

    if game_over:
        game_over_img = electolize_xlarge.render("Game Over", True, (255, 255, 255))
        x = display.get_width() / 2 - game_over_img.get_width() / 2
        y = display.get_height() / 2 - game_over_img.get_height() / 2
        display.blit(game_over_img, (x, y))

    pygame.display.update()
    clock.tick(60)
