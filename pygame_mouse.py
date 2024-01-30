import pygame

pygame.init()
basic_surface = pygame.display.set_mode((500, 500))

x = 250
y = 250
radius = 30
bg_color = (255, 255, 255)
circle_color = (0, 0, 0)

clock = pygame.time.Clock()


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
        if event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                radius += 5
            else:
                radius -= 5
        if event.type == pygame.WINDOWFOCUSLOST:
            bg_color = (100, 100, 100)

        if event.type == pygame.WINDOWFOCUSGAINED:
            bg_color = (255, 255, 255)

        if event.type == pygame.KEYDOWN:
            if event.key == 49:
                circle_color = (255, 0, 0)
            if event.key == 50:
                circle_color = (255, 155, 0)
            if event.key == 51:
                circle_color = (255, 255, 0)
            if event.key == 52:
                circle_color = (0, 255, 0)
            if event.key == 53:
                circle_color = (0, 0, 255)
            if event.key == 54:
                circle_color = (145, 0, 255)
            if event.key == pygame.K_ESCAPE:
                circle_color = (0, 0, 0)

    basic_surface.fill(bg_color)
    pygame.draw.circle(basic_surface, circle_color, (x, y), radius)

    pygame.display.update()
