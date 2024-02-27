import pygame
from pygame.surface import Surface
import json
from random import choice
from pacman_character import Pacman, Ghost
from typing import List

pygame.init()

display = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
fps = 10

map_surface = Surface((700, 500))
map = []
cell_size = pygame.Vector2(25, 25)


ghost_img = Surface((50, 50))
pygame.draw.circle(ghost_img, (255, 0, 0), (25, 20), 20)
pygame.draw.rect(ghost_img, (255, 0, 0), pygame.Rect((5, 25), (40, 35)))
pygame.draw.circle(ghost_img, (0, 0, 0), (11, 50), 7)
pygame.draw.circle(ghost_img, (0, 0, 0), (25, 50), 7)
pygame.draw.circle(ghost_img, (0, 0, 0), (38, 50), 7)
ghost_img.set_colorkey((0, 0, 0))


ghost_pos = pygame.Vector2(50, 50)

score = 0


dot_sound = pygame.mixer.Sound("./assets/coinsplash.ogg")


map = json.load(open("map.txt", "r"))


map_images = {i: pygame.image.load(f"assets/map-{i}.png") for i in range(10)}

for row_index in range(len(map)):
    for col_index in range(len(map[row_index])):
        x = col_index * 25
        y = row_index * 25
        value = map[row_index][col_index]
        rect = map_surface.blit(map_images[value], (x, y))
        # pygame.draw.rect(map_surface, (255, 0, 0), rect, 1)


pacman_img = pygame.transform.scale(pygame.image.load("./assets/pacman.png"), (50, 50))
pacman = Pacman(100, 100, pacman_img, display, map_surface, map, dot_sound)

ghosts: List[Ghost] = [
    Ghost(500, 500, ghost_img, display, map_surface, map, dot_sound),
    Ghost(100, 500, ghost_img, display, map_surface, map, dot_sound),
]

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

    pacman.step()

    display.fill((10, 10, 10))
    display.blit(map_surface, (0, 0))

    pacman.draw()

    for ghost in ghosts:
        next_pos = ghost.plan_next_pos(pacman.pos)
        ghost.pos = next_pos
        ghost.draw()

    pygame.display.update()
    clock.tick(fps)
