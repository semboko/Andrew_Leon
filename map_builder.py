import pygame
from pygame.surface import Surface
import json


pygame.init()

display = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
fps = 60

map = []
map_surface = Surface((700, 500))

for y in range(0, 500, 25):
    row = []
    for x in range(0, 700, 25):
       row.append(0)
    map.append(row)


map_images = {
    i: pygame.image.load(f"assets/map-{i}.png")
    for i in range(10)
}

for row_index in range(len(map)):
    for col_index in range(len(map[row_index])):
        x = col_index * 25
        y = row_index * 25
        value = map[row_index][col_index]
        map_surface.blit(map_images[value], (x, y))

def change_tile(map_surface, coords, img_number):
    tile_x = coords[1] * 25
    tile_y = coords[0] * 25
    map_surface.blit(Surface((25, 25)), (tile_x, tile_y))
    map_surface.blit(map_images[img_number], (tile_x, tile_y))
    return map_surface


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print("Saving the file...")
                content = json.dumps(map)
                output = open("map.txt", "w")
                output.write(content)
                output.close()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_x, click_y = event.pos
            col_idx = click_x // 25
            row_idx = click_y // 25
            map[row_idx][col_idx] += 1
            map[row_idx][col_idx] %= 10
            map_surface = change_tile(
                map_surface, (row_idx, col_idx), map[row_idx][col_idx]
            )

    display.fill((0, 0, 0))
    display.blit(map_surface, (0, 0))

    pygame.display.update()
    clock.tick(fps)
