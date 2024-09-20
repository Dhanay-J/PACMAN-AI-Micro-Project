
import time
import pygame
from settings import *

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.velocity = PACMAN_SPEED  # Pacman's velocity (moves per second)
        self.last_move_time = time.time()

    def move(self, game_map):
        current_time = time.time()
        if current_time - self.last_move_time >= 1 / self.velocity:
            new_x = max(0, min(self.x + self.direction[0], GRID_WIDTH - 1))
            new_y = max(0, min(self.y + self.direction[1], GRID_HEIGHT - 1))
            if not game_map.is_wall(new_x, new_y):
                self.x, self.y = new_x, new_y
            self.last_move_time = current_time

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)