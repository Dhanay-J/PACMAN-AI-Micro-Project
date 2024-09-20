import random
import pygame
from fruit import Fruit
from settings import *

class Map:
    def __init__(self, level):
        self.walls = set()
        self.fruits = []
        self.generate(level)

    def generate(self, level):
        # Add boundary walls
        for x in range(GRID_WIDTH):
            self.walls.add((x, 0))
            self.walls.add((x, GRID_HEIGHT - 1))
        for y in range(GRID_HEIGHT):
            self.walls.add((0, y))
            self.walls.add((GRID_WIDTH - 1, y))
        
        # Generate internal walls based on level
        num_walls = (level + 1) * 10
        for _ in range(num_walls):
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            self.walls.add((x, y))

    def is_wall(self, x, y):
        return (x, y) in self.walls

    def add_fruit(self, pacman, ghosts):
        while True:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            if not self.is_wall(x, y) and (x, y) != (pacman.x, pacman.y) and all((x, y) != (ghost.x, ghost.y) for ghost in ghosts):
                self.fruits.append(Fruit(x, y))
                break

    def remove_fruit(self, fruit):
        self.fruits.remove(fruit)

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for fruit in self.fruits:
            fruit.draw(screen)
