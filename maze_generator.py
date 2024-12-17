import pygame  # type: ignore
from random import choice

RES = WIDTH, HEIGHT = 1200, 900
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

WALL_COLOUR = "#0000ff"
VISITED_COLOUR = "#000000"
BACKGROUND_COLOUR = "#ffffff"
STACK_COLOUR = "#ff0000"
CURRENT_COLOUR = "#00ff00"
grid_cells = []


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(
            sc, pygame.Color(CURRENT_COLOUR), (x + 2, y + 2, TILE - 2, TILE - 2)
        )

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color(VISITED_COLOUR), (x, y, TILE, TILE))
        if self.walls["top"]:
            pygame.draw.line(sc, pygame.Color(WALL_COLOUR), (x, y), (x + TILE, y), 3)
        if self.walls["right"]:
            pygame.draw.line(
                sc, pygame.Color(WALL_COLOUR), (x + TILE, y), (x + TILE, y + TILE), 3
            )
        if self.walls["bottom"]:
            pygame.draw.line(
                sc, pygame.Color(WALL_COLOUR), (x + TILE, y + TILE), (x, y + TILE), 3
            )
        if self.walls["left"]:
            pygame.draw.line(sc, pygame.Color(WALL_COLOUR), (x, y + TILE), (x, y), 3)

    def check_cell(self, x, y):
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[y][x]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls["top"] = False
        next.walls["bottom"] = False
    elif dy == -1:
        current.walls["bottom"] = False
        next.walls["top"] = False


def generate_maze():
    for row in range(rows):
        grid_cells.append([Cell(col, row) for col in range(cols)])

    current_cell = grid_cells[0][0]
    stack = []

    while True:
        sc.fill(pygame.Color(BACKGROUND_COLOUR))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [cell.draw() for row in grid_cells for cell in row]
        current_cell.visited = True
        current_cell.draw_current_cell()
        for cell in stack:
            pygame.draw.rect(
                sc,
                pygame.Color(STACK_COLOUR),
                (cell.x * TILE + 2, cell.y * TILE + 2, TILE - 4, TILE - 4),
            )

        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()

        pygame.display.flip()
        clock.tick(1000)


generate_maze()