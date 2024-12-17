import pygame  # type: ignore
from random import choice
from maze_generator import *
import pickle


def load_maze(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def move(cur_cell, grid_cells):
    accessible = cur_cell.check_accessible(grid_cells)
    print(accessible)
    # new_cell = choice(neighbors)
    # return new_cell


def random_mouse_algorithm():
    grid_cells = load_maze("maze.pk1")
    cur_cell = grid_cells[0][0]
    print(cur_cell.walls)
    cur_cell = move(cur_cell, grid_cells)


def pygame_loop():
    grid_cells = load_maze("maze.pk1")
    while True:
        sc.fill(pygame.Color(BACKGROUND_COLOUR))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        draw_maze(grid_cells)

        pygame.display.flip()
        clock.tick(1000)


pygame_loop()
