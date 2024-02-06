import pygame
from pygame.surface import Surface
import json

pygame.init()

display = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
fps = 60

map_surface = Surface((700, 500))
map = []
cell_size = pygame.Vector2(25, 25)


map = json.load(open("map.txt", "r"))


map_images = {i: pygame.image.load(f"assets/map-{i}.png") for i in range(10)}

for row_index in range(len(map)):
    for col_index in range(len(map[row_index])):
        x = col_index * 25
        y = row_index * 25
        value = map[row_index][col_index]
        map_surface.blit(map_images[value], (x, y))


class Pacman:
    def __init__(self, x, y):
        # self.x = x
        # self.y = y
        self.pos = pygame.Vector2(x, y)

        self.angle = 0

        self.velocity = pygame.Vector2(0, 0)

        raw_image = pygame.image.load("assets/pacman.png")
        self.image = pygame.transform.scale(raw_image, (50, 50))

        self.pacman_rect = pygame.Rect(self.pos, self.image.get_size())

    def get_neighbor_cell(self, pacman_rect: pygame.Rect = None):
        pacman_rect = pacman_rect or self.pacman_rect
        cells = []
        for i in range(pacman_rect.left, pacman_rect.right, 25):
            for j in range(pacman_rect.top, pacman_rect.bottom, 25):
                v = i // 25
                h = j // 25
                cell = map[h][v]
                rect = pygame.Rect((v * 25, h * 25), (25, 25))
                cells.append(cell)
        return cells

    def get_neighbor_coordinates(self):
        result = []
        for i in range(self.pacman_rect.left, self.pacman_rect.right, 25):
            for j in range(self.pacman_rect.top, self.pacman_rect.bottom, 25):
                v = i // 25
                h = j // 25
                result.append((v, h))
        return result

    def handle_key(self, key: int):
        if key == pygame.K_UP:
            self.velocity = pygame.Vector2(0, -5)
            self.angle = 90

        if key == pygame.K_DOWN:
            self.velocity = pygame.Vector2(0, 5)
            self.angle = 270

        if key == pygame.K_LEFT:
            self.velocity = pygame.Vector2(-5, 0)
            self.angle = 180

        if key == pygame.K_RIGHT:
            self.velocity = pygame.Vector2(5, 0)
            self.angle = 0

    def step(self):
        next_pos = self.pos + self.velocity

        # wall_pos = next_pos - pygame.Vector2(25/2, 25/2)
        # wall_rect = pygame.Rect(wall_pos, (25, 25))

        # v = int(next_pos.x // 25)
        # h = int(next_pos.y // 25)

        # map_cell = map[h][v]
        next_rect = pygame.Rect(next_pos, self.pacman_rect.size)

        for map_cell in self.get_neighbor_cell(next_rect):
            if map_cell in (3, 4, 5, 6, 7, 8, 9):
                self.velocity = pygame.Vector2(0, 0)

        for v, h in self.get_neighbor_coordinates():
            if map[h][v] in (1, 2):
                map[h][v] = 0

        self.pos += self.velocity

        self.pos.x %= display.get_width()
        self.pos.y %= display.get_height()

    def handle_pressed_keys(self, pressed):
        if pressed[pygame.K_UP]:
            if self.y - 25 < 0:
                self.y = display.get_height() - 25
                return
            self.y -= 5
            self.angle = 90
        if pressed[pygame.K_DOWN]:
            if self.y + 25 > display.get_height():
                self.y = 25
                return
            self.y += 5
            self.angle = 270
        if pressed[pygame.K_LEFT]:
            if self.x - 25 < 0:
                self.x = display.get_width() - 25
                return
            self.x -= 5
            self.angle = 180
        if pressed[pygame.K_RIGHT]:
            if self.x + 25 > display.get_width():
                self.x = 25
                return
            self.x += 5
            self.angle = 0

    def draw(self):
        w = self.image.get_width()
        h = self.image.get_height()

        # position = (self.x - w/2, self.y - h/2)
        position = self.pos - pygame.Vector2(w / 2, h / 2)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.pacman_rect = display.blit(rotated_image, position)
        pygame.draw.rect(display, (255, 0, 0), self.pacman_rect, 1)


pacman = Pacman(100, 100)

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

    # pressed = pygame.key.get_pressed()
    # pacman.handle_pressed_keys(pressed)

    pacman.step()

    display.fill((10, 10, 10))
    display.blit(map_surface, (0, 0))

    pacman.draw()

    pygame.display.update()
    clock.tick(fps)
