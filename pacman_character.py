import pygame
from typing import Optional, Tuple


class Character:
    def __init__(self, x, y, img, display, map_surface, map, dot_sound):
        self.pos = pygame.Vector2(x, y)
        self.display = display
        self.dot_sound = dot_sound
        self.map = map
        self.map_surface = map_surface
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)
        self.image = img
        self.pacman_rect = pygame.Rect(self.pos, self.image.get_size())
        self.score = 0

    def get_neighbor_coordinates(self, pacman_rect: Optional[pygame.Rect] = None):
        pacman_rect = pacman_rect or self.pacman_rect
        result = []
        left = pacman_rect.left // 25 - 3
        top = pacman_rect.top // 25 - 3
        right = left + pacman_rect.width // 25 + 4
        bottom = top + pacman_rect.top // 25 + 4
        for v in range(left, right):
            for h in range(top, bottom):
                rect = pygame.Rect((v * 25, h * 25), (25, 25))
                if rect.colliderect(pacman_rect):
                    result.append((v, h))
        return result

    def overlap_any_wall(self, pos: Tuple[int, int]):
        h = (pos[1] // 25) % 500
        v = (pos[0] // 25) % 700
        try:
            return self.map[h][v] in (3, 4, 5, 6, 7, 8, 9)
        except IndexError:
            return True

    def step(self):
        next_pos = pygame.Vector2(self.pacman_rect.left, self.pacman_rect.top) + self.velocity
        next_rect = pygame.Rect(next_pos, self.pacman_rect.size)

        for v, h in self.get_neighbor_coordinates(next_rect):
            v %= 700//25
            h %= 500//25
            if self.map[h][v] in (3, 4, 5, 6, 7, 8, 9):
                self.velocity = pygame.Vector2(0, 0)

        for v, h in self.get_neighbor_coordinates():
            if self.map[h][v] in (1, 2):
                self.map[h][v] = 0
                rect = pygame.Rect((v * 25, h * 25), (25, 25))
                pygame.draw.rect(self.map_surface, (0, 0, 0), rect)
                self.dot_sound.set_volume(0.05)
                self.dot_sound.play()
                self.score += 5

        self.pos += self.velocity

        self.pos.x %= self.display.get_width()
        self.pos.y %= self.display.get_height()

    def draw(self):
        w = self.image.get_width()
        h = self.image.get_height()

        position = self.pos - pygame.Vector2(w / 2, h / 2)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.pacman_rect = self.display.blit(rotated_image, position)


class Pacman(Character):
    def handle_key(self, key: int):
        if key == pygame.K_UP:
            self.velocity = pygame.Vector2(0, -25)
            self.angle = 90

        if key == pygame.K_DOWN:
            self.velocity = pygame.Vector2(0, 25)
            self.angle = 270

        if key == pygame.K_LEFT:
            self.velocity = pygame.Vector2(-25, 0)
            self.angle = 180

        if key == pygame.K_RIGHT:
            self.velocity = pygame.Vector2(25, 0)
            self.angle = 0


class Ghost(Character):
    def plan_next_pos(self, packman_pos: pygame.Vector2):
        if packman_pos.distance_to(self.pos) < 25:
            return self.pos
        gscore, hscore, fscore, came_from = {}, {}, {}, {}
        current_pos = round(self.pos.x), round(self.pos.y)
        target = round(packman_pos.x), round(packman_pos.y)
        open_set, closed_set = {current_pos, }, set()

        gscore[current_pos] = 0
        hscore[current_pos] = self.pos.distance_to(packman_pos)
        fscore[current_pos] = gscore[current_pos] + hscore[current_pos]
        while open_set:
            spot = min(open_set, key=lambda x: fscore[x])
            if spot == target:
                rev_path = [target]
                while rev_path[-1] != current_pos:
                    rev_path.append(came_from[rev_path[-1]])
                return pygame.Vector2(rev_path[-2])

            open_set.remove(spot)
            closed_set.add(spot)

            neighbors = (
                (spot[0], spot[1] + 25),
                (spot[0], spot[1] - 25),
                (spot[0] + 25, spot[1]),
                (spot[0] - 25, spot[1]),
            )

            for n in neighbors:
                if n in open_set or n in closed_set:
                    continue
                if self.overlap_any_wall(n):
                    continue
                open_set.add(n)

                gscore[n] = gscore[spot] + 25
                hscore[n] = pygame.Vector2(n).distance_to(packman_pos)
                fscore[n] = gscore[n] + hscore[n]

                came_from[n] = spot
