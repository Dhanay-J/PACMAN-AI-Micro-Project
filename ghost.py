import random
import time
import pygame
from settings import *

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = GHOST_SPEED  # Start with a lower velocity
        self.last_move_time = time.time()

    def move(self, pacman, game_map, algorithm):
        current_time = time.time()
        if current_time - self.last_move_time >= 1 / self.velocity:
            path = algorithm(self, pacman, game_map)
            
            if path and len(path) > 1 and self.velocity/PACMAN_SPEED <= 0.9:  # 80% chance to move
                new_x, new_y = path[1]
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and not game_map.is_wall(new_x, new_y):
                    self.x, self.y = new_x, new_y
            self.last_move_time = current_time

            if self.velocity/PACMAN_SPEED == 0.9:
                self.increase_velocity(pacman.velocity)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def increase_velocity(self, pacman_velocity):
        # Increase velocity until it's 3 less than Pacman's
        if self.velocity < pacman_velocity - 10:
            self.velocity += 10  # Gradual increase
        else:
            if random.random() < 0.8:  # 60% chance to decrease
                self.velocity -= 20  # Sudden decrease
    