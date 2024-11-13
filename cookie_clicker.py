import pygame
from math import dist
from random import randint
from dataclasses import dataclass


pygame.init()
window = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

bg = pygame.image.load("./assets/bgBlue.jpg")
perfectCookie = pygame.image.load("./assets/perfectCookie.png")
perfectCookie = pygame.transform.scale_by(perfectCookie, 0.4)
icons = pygame.image.load("./assets/icons.png")
buildings = pygame.image.load("./assets/buildings.png")
storeTile = pygame.image.load("./assets/storeTile.jpg")

merriweather = pygame.font.Font("./assets/Merriweather-Regular.ttf", 50)

click_counter = 0
cookie_hitbox = pygame.Rect(0, 0, 0, 0)
cookieSizeFactor = 1


@dataclass
class ClickEvent:
    x: int
    y: int
    lifespan: int
    text: str


@dataclass
class ClickCookie:
    x: int
    y: int
    vel_x: int
    vel_y: int
    lifespan: int
    img: pygame.Surface


click_events: list[ClickEvent] = []
click_cookies: list[ClickCookie] = []


def onCookie(event):
    return dist(cookie_hitbox.center, event.pos) < cookie_hitbox.width/2


def get_icon(row, col):
    return icons.subsurface((48 * col, 48 * row, 48, 48))


def draw_shop():
    for i in range(8):
        tile = storeTile.subsurface((0, (i % 4) * 64, 300, 64))
        window.blit(tile, (500, i * 64))
        icon = buildings.subsurface((0, i * 64, 64, 64))
        window.blit(icon, (500, i * 64))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and onCookie(event):
            cookieSizeFactor = 0.95
            click_counter += 1
            ce_x = event.pos[0] - 30 + randint(-10, 10)
            ce_y = event.pos[1] - 40
            click_events.append(ClickEvent(ce_x, ce_y, 120, "+1"))
            click_cookies.append(ClickCookie(ce_x, ce_y, 0, -2, 120, get_icon(3, 0)))
        if event.type == pygame.MOUSEBUTTONUP:
            cookieSizeFactor *= 1.06
        if event.type == pygame.MOUSEMOTION:
            if onCookie(event):
                cookieSizeFactor = 1.1
            else:
                cookieSizeFactor = 1

    window.blit(bg, (0, 0))
    resizedCookie = pygame.transform.scale_by(perfectCookie, cookieSizeFactor)
    cookie_dest = resizedCookie.get_rect(center=(125, 250))
    cookie_hitbox = window.blit(resizedCookie, cookie_dest)

    counter_img = merriweather.render(str(click_counter), True, (255, 255, 255))
    counter_img_x = 25 + perfectCookie.get_width()/2 - counter_img.get_width()/2
    window.blit(counter_img, (counter_img_x, 50))

    for ce in click_events:
        ce_img = merriweather.render(ce.text, True, (255, 255, 255))
        ce_img.set_alpha(2 * ce.lifespan)
        window.blit(ce_img, (ce.x, ce.y))
        ce.y -= 1
        ce.lifespan -= 1
        if ce.lifespan == 0:
            click_events.remove(ce)

    for cc in click_cookies:
        cc.img.set_alpha(cc.vel_y * -120 - 120)
        window.blit(cc.img, (cc.x, cc.y))
        cc.y -= cc.vel_y
        cc.vel_y += 0.01
        if cc.vel_y > 0:
            click_cookies.remove(cc)

    draw_shop()

    pygame.display.update()
    clock.tick(60)
