import pygame
from random import randint


pygame.init()
display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

bg_img = pygame.image.load("./assets/fj_bg.jpg")
w, h = bg_img.get_size()
scale_factor = 0.7
bg_img = pygame.transform.scale(bg_img, (w * scale_factor, h * scale_factor))


electolize_large = pygame.font.Font("./assets/Electrolize-Regular.ttf", 40)
score = 0

fruit_imgs = []

for fruit_name in ("apple", "banana", "peach", "strawberry", "watermelon"):
    file_name = "./assets/" + fruit_name + ".png"
    img = pygame.image.load(file_name)
    fruit_imgs.append(img)

fruits = []


def spawn_fruit():
    kind = randint(0, 4)
    fruit_width = fruit_imgs[kind].get_width()
    x = randint(0, 500 - fruit_width)
    y = randint(-500, -100)
    fruits.append([x, y, kind, 0])


for _ in range(5):
    spawn_fruit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for fruit in fruits:
                x, y, kind, *_ = fruit
                fi = fruit_imgs[kind]
                fruit_hitbox = pygame.Rect((x, y), fi.get_size())
                if fruit_hitbox.collidepoint(event.pos):
                    fruits.remove(fruit)
                    score += 2

    display.blit(bg_img, (-340, 0))
    for f in fruits:
        img = fruit_imgs[f[2]]
        display.blit(img, (f[0], f[1]))
        f[1] = f[1] + f[3]
        f[3] = f[3] + 0.028

    score_img = electolize_large.render("Score: " + str(score), True, (255, 255, 255))
    display.blit(score_img, (0, 0))

    if randint(0, 45) == 0:
        spawn_fruit()

    pygame.display.update()
    clock.tick(60)
