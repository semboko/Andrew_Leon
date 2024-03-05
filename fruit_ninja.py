import pygame


pygame.init()
display = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()

bg_img = pygame.image.load("./assets/fj_bg.jpg")
w, h = bg_img.get_size()
scale_factor = 0.6
bg_img = pygame.transform.scale(bg_img, (w * scale_factor, h * scale_factor))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    display.blit(bg_img, (-340, 0))

    pygame.display.update()
    clock.tick(60)
